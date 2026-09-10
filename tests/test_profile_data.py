import datetime as dt
import tempfile
import unittest
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from unittest.mock import patch

from scripts.profile_data import main, render_counters, resolved_issues
from scripts.public_calendar import add_public_days


def pr(
    private=False, issue_private=False, closed=True, closed_at="2026-09-10T00:00:01Z"
):
    return {
        "repository": {"isPrivate": private},
        "mergedAt": "2026-09-10T00:00:00Z",
        "closingIssuesReferences": {
            "pageInfo": {"hasNextPage": False},
            "nodes": [
                {
                    "id": "issue1",
                    "repository": {"isPrivate": issue_private},
                    "closed": closed,
                    "closedAt": closed_at,
                }
            ],
        },
    }


class ProfileDataTests(unittest.TestCase):
    def test_resolution_deduplicates_and_filters_private_and_prior_closure(self):
        self.assertEqual(resolved_issues([pr(), pr()]), {"issue1"})
        for item in [
            pr(private=True),
            pr(issue_private=True),
            pr(closed=False),
            pr(closed_at="2026-09-09T00:00:00Z"),
        ]:
            self.assertEqual(resolved_issues([item]), set())

    def test_truncated_references_fail(self):
        item = pr()
        item["closingIssuesReferences"]["pageInfo"]["hasNextPage"] = True
        with self.assertRaises(ValueError):
            resolved_issues([item])

    def test_calendar_ignores_private_and_restricted_records(self):
        days = Counter()
        add_public_days(
            days,
            [
                {"isRestricted": True},
                {
                    "isRestricted": False,
                    "occurredAt": "2026-09-10T00:00:00Z",
                    "repository": {"isPrivate": True},
                },
                {
                    "isRestricted": False,
                    "occurredAt": "2026-09-10T00:00:00Z",
                    "repository": {"isPrivate": False},
                    "commitCount": 3,
                },
            ],
        )
        self.assertEqual(dict(days), {"2026-09-10": 3})

    def test_failed_fetch_preserves_previous_files(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "counters.svg"
            target.write_text("previous")
            with (
                patch(
                    "scripts.profile_data.fetch_counters",
                    side_effect=RuntimeError("offline"),
                ),
                patch("sys.argv", ["profile_data", directory]),
                self.assertRaises(RuntimeError),
            ):
                main()
            self.assertEqual(target.read_text(), "previous")

    def test_fixture_build_writes_parseable_graphics(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            patch("scripts.profile_data.fetch_counters", return_value=(10, 8, 6)),
            patch(
                "scripts.profile_data.fetch_calendar",
                return_value=(dt.date(2026, 9, 10), {"2026-09-10": 3}),
            ),
            patch("scripts.profile_data.subprocess.check_output", return_value="[[]]"),
            patch("sys.argv", ["profile_data", directory]),
        ):
            main()
            for name in ("counters.svg", "calendar.svg"):
                ET.parse(Path(directory) / name)
            self.assertIn("10", (Path(directory) / "README.md").read_text())

    def test_svg_escapes_text(self):
        root = ET.fromstring(render_counters((10, 8, 6), "<&>"))
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")


if __name__ == "__main__":
    unittest.main()
