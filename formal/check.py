#!/usr/bin/env python3
"""Check source correspondence, real Git behavior, and the bounded model."""

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JAR_HASH = "936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88"
URL = "https://github.com/tlaplus/tlaplus/releases/download/v1.7.4/tla2tools.jar"


def run(args, cwd=ROOT):
    result = subprocess.run(
        args,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(result.stdout, end="", flush=True)
    return result


def main():
    for line in (ROOT / "formal/source.sha256").read_text().splitlines():
        expected, path = line.split("  ", 1)
        actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        if expected != actual:
            sys.exit(f"Source drift: {path}; review mapping before updating the hash")
    cache = Path(
        os.environ.get(
            "TLA2TOOLS", Path.home() / ".cache/profile-publication/tla2tools-1.7.4.jar"
        )
    )
    if not cache.exists():
        cache.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(URL) as source:
            data = source.read()
        if hashlib.sha256(data).hexdigest() != JAR_HASH:
            sys.exit("TLC download hash mismatch")
        cache.write_bytes(data)
    if hashlib.sha256(cache.read_bytes()).hexdigest() != JAR_HASH:
        sys.exit("TLC jar hash mismatch")
    java = os.environ.get("JAVA", "java")
    if run(
        [
            sys.executable,
            "-m",
            "unittest",
            "tests.test_publication",
            "tests.test_formal_publication",
            "-v",
        ]
    ).returncode:
        sys.exit("Publication fixture failed")
    with tempfile.TemporaryDirectory(prefix="publication-proof-") as temp:
        scratch = Path(temp)
        (scratch / ".github/workflows").mkdir(parents=True)
        shutil.copytree(
            ROOT / "tests",
            scratch / "tests",
            ignore=shutil.ignore_patterns("__pycache__"),
        )
        workflow = (ROOT / ".github/workflows/profile.yml").read_text()
        needle = '          cp "$GENERATED/cadence-mobile.svg" cadence-mobile.svg\n'
        if workflow.count(needle) != 1:
            sys.exit("Mutation site changed; review mapping")
        (scratch / ".github/workflows/profile.yml").write_text(
            workflow.replace(needle, "")
        )
        mutation = run(
            [sys.executable, "-m", "unittest", "tests.test_publication", "-v"], scratch
        )
        if (
            mutation.returncode == 0
            or "previous" not in mutation.stdout
            or "current cadence-mobile.svg" not in mutation.stdout
        ):
            sys.exit(
                "Real workflow mutation did not expose the expected mixed snapshot"
            )
        for cfg, should_pass in (("pass.cfg", True), ("mutant.cfg", False)):
            result = run(
                [
                    java,
                    "-XX:+UseParallelGC",
                    "-cp",
                    str(cache),
                    "tlc2.TLC",
                    "-workers",
                    "1",
                    "-config",
                    str(ROOT / "formal" / cfg),
                    str(ROOT / "formal/Publication.tla"),
                ],
                scratch,
            )
            if should_pass and (
                result.returncode or "No error has been found" not in result.stdout
            ):
                sys.exit("Model check failed")
            if not should_pass and (
                result.returncode == 0
                or "Invariant CompleteSnapshot is violated" not in result.stdout
            ):
                sys.exit("Model mutation did not violate CompleteSnapshot")
    print("Source, real Git fixture, and model mutation checks passed.")


if __name__ == "__main__":
    main()
