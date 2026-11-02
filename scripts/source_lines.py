"""Physical source lines in selected public repository archives, at recorded commits."""

import hashlib
import json
import os
import re
import shutil
import subprocess
import tarfile
import tempfile
import time
import urllib.request
from pathlib import Path, PurePosixPath

TOOL = {
    "name": "cloc",
    "version": "2.10",
    "sha256": "bf59272455172108072a0a106379f7509fd4349bdcfd85203bac038ccd286d83",
    "source": "https://raw.githubusercontent.com/AlDanial/cloc/eb5cef64db2b2d4380f501568cc584b7cab4ba50/cloc",
}
EXCLUDED_DIRS = [
    ".git",
    ".hg",
    ".svn",
    ".bzr",
    ".cvs",
    ".snapshot",
    "node_modules",
    "vendor",
    "dist",
    "build",
    ".next",
    ".open-next",
    ".venv",
    "venv",
    "coverage",
    "__pycache__",
    ".terraform",
    "site-packages",
]
RULES = {
    "excluded_dirs": EXCLUDED_DIRS,
    "exclude_known_generated": True,
    "count_duplicate_files": True,
    "follow_links": False,
}
RULES["sha256"] = hashlib.sha256(json.dumps(RULES, sort_keys=True).encode()).hexdigest()
FIELDS = ("files", "code", "comment", "blank")
SELECTED = frozenset(
    (
        "Jerome-Group/algebra",
        "Jerome-Group/calculus",
        "jerome-queck/probability",
        "Jerome-Group/numbertheory",
        "Jerome-Group/calculator",
        "Jerome-Group/ntulearn",
        "Jerome-Group/academic-os",
        "Jerome-Group/syrax",
        "jerome-queck/emmy",
    )
)


def download(url, target, limit):
    with (
        urllib.request.urlopen(url, timeout=45) as response,
        target.open("wb") as output,
    ):
        size = 0
        started = time.monotonic()
        while chunk := response.read(1024 * 1024):
            size += len(chunk)
            if time.monotonic() - started > 90:
                raise TimeoutError("Source download exceeds time bound")
            if size > limit:
                raise ValueError("Source download exceeds size bound")
            output.write(chunk)


def counter_path():
    cache = Path(os.environ.get("RUNNER_TEMP", tempfile.gettempdir())) / "profile-cloc"
    cache.mkdir(parents=True, exist_ok=True)
    target = cache / (TOOL["sha256"] + ".pl")
    if not target.exists():
        with tempfile.TemporaryDirectory(dir=cache) as directory:
            incoming = Path(directory) / "cloc.pl"
            download(TOOL["source"], incoming, 2 * 1024 * 1024)
            if hashlib.sha256(incoming.read_bytes()).hexdigest() != TOOL["sha256"]:
                raise ValueError("Source counter checksum mismatch")
            incoming.replace(target)
    if hashlib.sha256(target.read_bytes()).hexdigest() != TOOL["sha256"]:
        raise ValueError("Source counter checksum mismatch")
    return target


def unpack_archive(archive, destination):
    regular, links, size = 0, 0, 0
    seen = set()
    root = None
    with tarfile.open(archive, "r:gz") as source:
        for index, member in enumerate(source):
            if index >= 100000:
                raise ValueError("Source archive exceeds file bound")
            path = PurePosixPath(member.name)
            if (
                path.is_absolute()
                or ".." in path.parts
                or not path.parts
                or "\\" in member.name
            ):
                raise ValueError("Unsafe source archive path")
            if root is None:
                root = path.parts[0]
            if path.parts[0] != root or member.name in seen:
                raise ValueError("Inconsistent source archive root or duplicate path")
            seen.add(member.name)
            if member.issym() or member.islnk():
                links += 1
                continue
            if member.isdir():
                continue
            if not member.isfile() or len(path.parts) < 2:
                raise ValueError("Unsupported source archive member")
            regular += 1
            size += member.size
            if size > 600 * 1024 * 1024:
                raise ValueError("Expanded source archive exceeds size bound")
            target = destination.joinpath(*path.parts[1:])
            target.parent.mkdir(parents=True, exist_ok=True)
            with source.extractfile(member) as content, target.open("xb") as output:
                shutil.copyfileobj(content, output)
    return regular, links


def totals(languages):
    return {field: sum(row[field] for row in languages.values()) for field in FIELDS}


def validate_counts(row):
    if (
        not isinstance(row, dict)
        or set(row) != set(FIELDS)
        or any(type(row[field]) is not int or row[field] < 0 for field in FIELDS)
    ):
        raise ValueError("Invalid source line counts")


def parse_report(report, allow_empty=False):
    if report == {} and allow_empty:
        return {}
    if not isinstance(report, dict):
        raise TypeError("Invalid source counter report")
    if "header" not in report or not isinstance(report["header"], dict):
        raise ValueError("Incomplete source counter report")
    if report["header"].get("cloc_version") != TOOL["version"]:
        raise ValueError("Unexpected source counter version")
    languages = {}
    for name, row in report.items():
        if name in ("header", "SUM"):
            continue
        if not isinstance(name, str) or not name or not isinstance(row, dict):
            raise ValueError("Invalid source language record")
        converted = {
            "files": row.get("nFiles"),
            **{key: row.get(key) for key in FIELDS[1:]},
        }
        validate_counts(converted)
        languages[name] = converted
    summary = report.get("SUM")
    if summary is None:
        raise ValueError("Incomplete source counter total")
    expected = {
        "files": summary.get("nFiles"),
        **{key: summary.get(key) for key in FIELDS[1:]},
    }
    validate_counts(expected)
    if expected != totals(languages):
        raise ValueError("Source counter totals disagree")
    return languages


def count_directory(directory, tool):
    result = subprocess.run(
        [
            "perl",
            str(tool),
            "--config=/dev/null",
            "--json",
            "--quiet",
            "--timeout=0",
            "--skip-uniqueness",
            "--no-autogen",
            "--exclude-dir=" + ",".join(EXCLUDED_DIRS),
            str(directory),
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=90,
    )
    if result.stderr.strip():
        raise ValueError("Source counter reported an error")
    return parse_report(json.loads(result.stdout), allow_empty=True)


def combine(records):
    languages = {}
    for record in records:
        for name, row in record["by_language"].items():
            aggregate = languages.setdefault(name, dict.fromkeys(FIELDS, 0))
            for field in FIELDS:
                aggregate[field] += row[field]
    return dict(sorted(languages.items()))


def collect_source_lines(projects):
    if len(projects) != len(SELECTED) or {p["repo"] for p in projects} != SELECTED:
        raise ValueError(
            "Source counting requires the nine selected public repositories"
        )
    tool = counter_path()
    records = []
    for project in projects:
        repo, head = project["repo"], project["head"]["oid"]
        if not re.fullmatch(r"[0-9a-f]{40}", head):
            raise ValueError("Source counting requires a recorded commit SHA")
        url = f"https://codeload.github.com/{repo}/tar.gz/{head}"
        with tempfile.TemporaryDirectory(prefix="profile-source-") as directory:
            directory = Path(directory)
            archive, tree = directory / "source.tar.gz", directory / "tree"
            tree.mkdir()
            download(url, archive, 150 * 1024 * 1024)
            files, links = unpack_archive(archive, tree)
            languages = count_directory(tree, tool)
        counted = totals(languages)
        records.append(
            {
                "repo": repo,
                "head": head,
                "source_url": url,
                "archive_files": files,
                "skipped_links": links,
                "uncounted_files": files - counted["files"],
                "by_language": languages,
                "totals": counted,
            }
        )
    languages = combine(records)
    result = {
        "tool": TOOL.copy(),
        "rules": RULES.copy(),
        "repositories": records,
        "by_language": languages,
        "totals": totals(languages),
    }
    validate_source_lines(result, projects)
    return result


def validate_source_lines(source, projects):
    if source["tool"] != TOOL or source["rules"] != RULES:
        raise ValueError("Source counting provenance mismatch")
    records = source["repositories"]
    if len(records) != len(projects) or len({r["repo"] for r in records}) != len(
        records
    ):
        raise ValueError("Incomplete source repository coverage")
    expected = {p["repo"]: p["head"]["oid"] for p in projects}
    for record in records:
        repo, head = record["repo"], record["head"]
        if (
            repo not in SELECTED
            or expected.get(repo) != head
            or not re.fullmatch(r"[0-9a-f]{40}", head)
        ):
            raise ValueError("Source repository identity or commit mismatch")
        if record["source_url"] != f"https://codeload.github.com/{repo}/tar.gz/{head}":
            raise ValueError("Source archive provenance mismatch")
        for name, row in record["by_language"].items():
            if not isinstance(name, str) or not name:
                raise ValueError("Invalid source language")
            validate_counts(row)
        validate_counts(record["totals"])
        if record["totals"] != totals(record["by_language"]):
            raise ValueError("Source repository totals disagree")
        for field in ("archive_files", "skipped_links", "uncounted_files"):
            if type(record[field]) is not int or record[field] < 0:
                raise ValueError("Invalid archive file counts")
        if (
            record["archive_files"]
            != record["uncounted_files"] + record["totals"]["files"]
        ):
            raise ValueError("Archive file totals disagree")
    if source["by_language"] != combine(records) or source["totals"] != totals(
        source["by_language"]
    ):
        raise ValueError("Aggregate source counts disagree")
    for row in source["by_language"].values():
        validate_counts(row)
    validate_counts(source["totals"])


def markdown_source_lines(source):
    summary = source["totals"]
    lines = [
        "## Classified source lines",
        "",
        (
            "Physical lines at the nine recorded public project commits, across all authors. "
            "cloc classifies code, comments and blanks; plain text, markup and configuration may count as code. "
            "These are repository contents, not lines written by Jerome or expertise. "
            "Declared dependency/build directories and cloc's known generated files are excluded; "
            "other generated or vendored material may remain. Unrecognized/binary files and links are not counted."
        ),
        "",
        f"Counter: [cloc {TOOL['version']}]({TOOL['source']}), SHA-256 `{TOOL['sha256']}`.",
        f"Rules SHA-256: `{RULES['sha256']}`. Excluded directories: "
        + ", ".join(f"`{d}`" for d in EXCLUDED_DIRS)
        + ".",
        "",
        "Totals: " + ", ".join(f"{summary[field]:,} {field}" for field in FIELDS) + ".",
        "",
        "| Language | Files | Code | Comments | Blanks |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for language, row in sorted(
        source["by_language"].items(), key=lambda item: (-item[1]["code"], item[0])
    ):
        lines.append(
            "| "
            + language.replace("|", "&#124;")
            + " | "
            + " | ".join(f"{row[field]:,}" for field in FIELDS)
            + " |"
        )
    lines += ["", "### Source commits", ""]
    for record in source["repositories"]:
        lines.append(
            f"- [{record['repo']} @ {record['head']}]({record['source_url']}): "
            + ", ".join(f"{record['totals'][field]:,} {field}" for field in FIELDS)
            + f"; {record['uncounted_files']:,} uncounted files; {record['skipped_links']:,} skipped links."
        )
    return "\n".join(lines)
