import datetime as dt
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch

from scripts.profile_data import main, merge_months, render_snapshot
from scripts.upstream_prs import fetch_upstream
from tests.test_upstream_prs import node


def snapshot():
    today = dt.date(2026, 11, 2)
    record = node(state="MERGED")
    upstream = fetch_upstream(
        lambda *a, **kw: {
            "search": {
                "issueCount": 1,
                "nodes": [record],
                "pageInfo": {"hasNextPage": False},
            }
        }
    )
    return {
        "schema_version": 3,
        "observed_from": "2026-11-02T00:00:00+00:00",
        "observed_to": "2026-11-02T00:01:00+00:00",
        "updated": "02 Nov 2026 00:01 UTC",
        "counts": [10, 8, 6],
        "calendar_start": "2026-07-01",
        "calendar_end": str(today),
        "calendar_days": {"2026-11-02": 3},
        "calendar_kinds": {
            "commits": 3,
            "issues": 0,
            "pull_requests": 0,
            "reviews": 0,
            "repositories": 0,
        },
        "merge_months": merge_months({"2026-11-01": 2}, today),
        "projects": [],
        "recent_events": [],
        "upstream_prs": upstream,
    }


class SnapshotV3Tests(unittest.TestCase):
    def test_new_metrics_and_native_sources_share_one_input(self):
        source = snapshot()
        files = render_snapshot(source)
        self.assertEqual(len(files), 15)
        self.assertEqual(json.loads(files["snapshot.json"]), source)
        self.assertIn("1 merged, 0 open, 0 closed without merge", files["README.md"])
        self.assertIn("including 1 upstream", files["README.md"])
        self.assertIn("https://github.com/upstream/project/pull/1", files["README.md"])
        self.assertIn("天気", files["README.md"])
        self.assertIn("Mon: 3", files["README.md"])
        self.assertIn("commits: 3", files["README.md"])
        self.assertIn(
            "1 PRs, 12 added lines, 3 deleted lines, 2 file changes", files["README.md"]
        )
        self.assertIn("patch +12/−3, 2 file changes", files["README.md"])
        self.assertEqual(files, render_snapshot(source))

    def test_missing_new_sources_never_turn_into_zero(self):
        for key in ("schema_version", "upstream_prs", "calendar_kinds"):
            source = snapshot()
            source.pop(key)
            with self.assertRaises((ValueError, KeyError)):
                render_snapshot(source)
        source = snapshot()
        source["schema_version"] = 1
        with self.assertRaisesRegex(ValueError, "schema-v3"):
            render_snapshot(source)
        source = snapshot()
        source["projects"] = [{"name": "Algebra", "head": None, "release": None}]
        with self.assertRaises(KeyError):
            render_snapshot(source)

    def test_missing_or_invalid_patch_statistics_fail_before_publication(self):
        for field in ("additions", "deletions", "changed_files"):
            source = snapshot()
            source["upstream_prs"][0].pop(field)
            with self.assertRaises(KeyError):
                render_snapshot(source)
            for value in (True, -1, None):
                source = snapshot()
                source["upstream_prs"][0][field] = value
                with self.assertRaises(ValueError):
                    render_snapshot(source)

    def test_mismatched_invalid_or_missing_activity_mix_fails(self):
        for value in (
            {},
            {
                "commits": True,
                "issues": 0,
                "pull_requests": 0,
                "reviews": 0,
                "repositories": 0,
            },
            {
                "commits": 2,
                "issues": 0,
                "pull_requests": 0,
                "reviews": 0,
                "repositories": 0,
            },
        ):
            source = snapshot()
            source["calendar_kinds"] = value
            with self.assertRaises(ValueError):
                render_snapshot(source)
        source = snapshot()
        source["schema_version"] = 2
        with self.assertRaisesRegex(ValueError, "schema-v3"):
            render_snapshot(source)

    def test_render_failure_leaves_existing_output_untouched(self):
        source = snapshot()
        source["recent_events"] = [
            {
                "repo": "\U0010ffff",
                "number": 1,
                "action": "opened",
                "date": "2026-11-02",
            }
        ]
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "snapshot.json"
            target.write_text("previous successful publication")
            with (
                patch("scripts.profile_data.collect_snapshot", return_value=source),
                patch("sys.argv", ["profile_data", directory]),
                self.assertRaisesRegex(ValueError, "Unsupported glyph"),
            ):
                main()
            self.assertEqual(target.read_text(), "previous successful publication")
            self.assertEqual(list(Path(directory).iterdir()), [target])

    def test_all_composed_type_ink_fits_and_paths_are_local(self):
        documents = []
        documents += [
            content
            for name, content in render_snapshot(snapshot()).items()
            if name.endswith(".svg")
        ]
        for document in documents:
            root = ET.fromstring(document)
            width, height = float(root.get("width")), float(root.get("height"))
            ids = {element.get("id") for element in root.iter() if element.get("id")}
            boxes = []
            for element in root.iter():
                if element.get("data-bounds"):
                    x, y, right, bottom = map(float, element.get("data-bounds").split())
                    self.assertGreaterEqual(x, 0, element.get("aria-label"))
                    self.assertGreaterEqual(y, 0, element.get("aria-label"))
                    self.assertLessEqual(right, width, element.get("aria-label"))
                    self.assertLessEqual(bottom, height, element.get("aria-label"))
                    boxes.append(element)
                if element.tag.endswith("use"):
                    self.assertIn(element.get("href")[1:], ids)
            self.assertTrue(boxes)
            self.assertNotIn("font-family", document)
            self.assertNotIn("<text", document)
            self.assertLess(
                len(document.encode()),
                1_000_000 if root.get("data-snapshot") else 300_000,
            )


if __name__ == "__main__":
    unittest.main()
