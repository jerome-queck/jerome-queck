import copy
import io
import json
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.source_lines import (
    FIELDS,
    RULES,
    SELECTED,
    TOOL,
    collect_source_lines,
    count_directory,
    counter_path,
    parse_report,
    totals,
    unpack_archive,
    validate_source_lines,
)


def empty_source():
    return {
        "tool": TOOL.copy(),
        "rules": RULES.copy(),
        "repositories": [],
        "by_language": {},
        "totals": dict.fromkeys(FIELDS, 0),
    }


def report():
    return {
        "header": {"cloc_version": "2.10"},
        "Python": {"nFiles": 1, "code": 1, "comment": 1, "blank": 1},
        "SUM": {"nFiles": 1, "code": 1, "comment": 1, "blank": 1},
    }


class SourceLinesTests(unittest.TestCase):
    def test_report_requires_version_nonnegative_integer_counts_and_full_totals(self):
        self.assertEqual(parse_report(report())["Python"], dict.fromkeys(FIELDS, 1))
        for bad in ({}, {"header": {}}, {"header": {"cloc_version": "2.10"}}):
            with self.assertRaises(ValueError):
                parse_report(bad)
        for value in (True, -1, 1.2, None):
            bad = report()
            bad["Python"]["code"] = value
            with self.assertRaises(ValueError):
                parse_report(bad)
        bad = report()
        bad["SUM"]["code"] += 1
        with self.assertRaises(ValueError):
            parse_report(bad)

    def test_no_unselected_or_private_archive_requested(self):
        with patch("scripts.source_lines.download") as download:
            for projects in (
                [],
                [{"repo": "private/secret", "head": {"oid": "a" * 40}}],
            ):
                with self.assertRaises(ValueError):
                    collect_source_lines(projects)
            download.assert_not_called()

    def test_unavailable_public_archive_cannot_become_zero(self):
        from urllib.error import HTTPError

        projects = [
            {"repo": repo, "head": {"oid": "a" * 40}} for repo in sorted(SELECTED)
        ]
        with (
            patch("scripts.source_lines.counter_path", return_value=Path("counter")),
            patch(
                "scripts.source_lines.download",
                side_effect=HTTPError("public-archive", 404, "Unavailable", {}, None),
            ),
            patch("scripts.source_lines.count_directory") as count,
            self.assertRaises(HTTPError),
        ):
            collect_source_lines(projects)
        count.assert_not_called()

    def test_archive_refuses_traversal_and_skips_links_without_following(self):
        for name in (
            "../escape.py",
            "/absolute.py",
            "repo/../escape.py",
            "repo\\escape.py",
        ):
            with tempfile.TemporaryDirectory() as directory:
                archive = Path(directory) / "repo.tar.gz"
                with tarfile.open(archive, "w:gz") as output:
                    info = tarfile.TarInfo(name)
                    info.size = 1
                    output.addfile(info, io.BytesIO(b"x"))
                with self.assertRaises(ValueError):
                    unpack_archive(archive, Path(directory) / "tree")
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "repo.tar.gz"
            tree = Path(directory) / "tree"
            tree.mkdir()
            with tarfile.open(archive, "w:gz") as output:
                info = tarfile.TarInfo("repo/link.py")
                info.type, info.linkname = tarfile.SYMTYPE, "/etc/passwd"
                output.addfile(info)
            self.assertEqual(unpack_archive(archive, tree), (0, 1))
            self.assertEqual(list(tree.iterdir()), [])

    def test_counter_failure_timeout_and_truncated_json_propagate(self):
        for error in (
            subprocess.TimeoutExpired("perl", 90),
            subprocess.CalledProcessError(1, "perl"),
        ):
            with (
                patch("scripts.source_lines.subprocess.run", side_effect=error),
                self.assertRaises(type(error)),
            ):
                count_directory(Path("fixture"), Path("counter"))
        for stdout, stderr in (("{", ""), (json.dumps(report()), "counter error")):
            with (
                patch(
                    "scripts.source_lines.subprocess.run",
                    return_value=subprocess.CompletedProcess([], 0, stdout, stderr),
                ),
                self.assertRaises(ValueError),
            ):
                count_directory(Path("fixture"), Path("counter"))

    def test_source_snapshot_refuses_identity_provenance_and_aggregate_drift(self):
        source = empty_source()
        repo, head = "Jerome-Group/algebra", "a" * 40
        languages = parse_report(report())
        record = {
            "repo": repo,
            "head": head,
            "source_url": f"https://codeload.github.com/{repo}/tar.gz/{head}",
            "archive_files": 2,
            "skipped_links": 0,
            "uncounted_files": 1,
            "by_language": languages,
            "totals": totals(languages),
        }
        source.update(
            repositories=[record], by_language=languages, totals=totals(languages)
        )
        projects = [{"repo": repo, "head": {"oid": head}}]
        validate_source_lines(source, projects)
        for mutate in (
            lambda s: s["repositories"][0].update(head="b" * 40),
            lambda s: s["repositories"][0].update(repo="private/secret"),
            lambda s: s["totals"].update(code=99),
            lambda s: s["totals"].update(code=True),
            lambda s: s["repositories"][0].update(uncounted_files=-1),
            lambda s: s["tool"].update(version="latest"),
        ):
            bad = copy.deepcopy(source)
            mutate(bad)
            with self.assertRaises(ValueError):
                validate_source_lines(bad, projects)

    def test_language_view_keeps_ten_names_and_exact_other_code_lines(self):
        import xml.etree.ElementTree as ET

        from scripts.readme_world import _languages
        from scripts.source_lines import markdown_source_lines

        source = empty_source()
        source["by_language"] = {
            f"Lang{i:02}": {"files": 1, "code": 20 - i, "comment": 2, "blank": 3}
            for i in range(12)
        }
        source["totals"] = totals(source["by_language"])
        document, _ = _languages({"source_lines": source}, 480, 0)
        labels = {
            node.get("aria-label")
            for node in ET.fromstring("<svg>" + document + "</svg>").iter()
        }
        for i in range(10):
            self.assertIn(f"Lang{i:02}", labels)
        self.assertNotIn("Lang10", labels)
        self.assertNotIn("Lang11", labels)
        self.assertIn("Other: 19 code lines", labels)
        native = markdown_source_lines(source)
        self.assertIn("Lang10", native)
        self.assertIn("Lang11", native)

    def test_tool_checksum_failure_never_runs_downloaded_code(self):
        with tempfile.TemporaryDirectory() as directory:

            def corrupt(url, target, limit):
                target.write_text("not the pinned tool")

            with (
                patch.dict("os.environ", {"RUNNER_TEMP": directory}),
                patch("scripts.source_lines.download", side_effect=corrupt),
                self.assertRaisesRegex(ValueError, "checksum"),
            ):
                counter_path()

    def test_actual_pinned_counter_separates_code_comments_blanks_and_excludes_dependencies(
        self,
    ):
        with tempfile.TemporaryDirectory() as directory:
            tree = Path(directory)
            (tree / "fixture.py").write_text("# comment\n\nx = 1\n")
            (tree / "same.py").write_text("# comment\n\nx = 1\n")
            (tree / "a.js").write_text("// comment\n\nconst x = 1;\n")
            (tree / "node_modules").mkdir()
            (tree / "node_modules" / "ignored.py").write_text("x = 2\n")
            actual = count_directory(tree, counter_path())
            self.assertEqual(actual["Python"], dict.fromkeys(FIELDS, 2))
            self.assertEqual(actual["JavaScript"], dict.fromkeys(FIELDS, 1))
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "binary.unknown").write_bytes(b"\x00\x01")
            self.assertEqual(count_directory(Path(directory), counter_path()), {})
