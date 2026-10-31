import datetime as dt
import tempfile
import unittest
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from unittest.mock import patch

from scripts.profile_data import (
    fetch_contributions,
    main,
    merge_months,
    render_counters,
    render_snapshot,
    resolved_issues,
)
from scripts.public_calendar import add_public_days, fetch_calendar, render_calendar
from scripts.recent_activity import markdown_activity, render_activity, select_activity


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
                    "scripts.profile_data.fetch_contributions",
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
            patch(
                "scripts.profile_data.fetch_contributions",
                return_value={"counts": [10, 8, 6], "merged_dates": {}},
            ),
            patch(
                "scripts.profile_data.fetch_calendar",
                return_value=(dt.date(2026, 9, 10), {"2026-09-10": 3}),
            ),
            patch("scripts.profile_data.fetch_activity", return_value=[]),
            patch("scripts.profile_data.load_projects", return_value=[]),
            patch("sys.argv", ["profile_data", directory]),
        ):
            main()
            for name in ("counters.svg", "calendar.svg"):
                ET.parse(Path(directory) / name)
            self.assertIn("10", (Path(directory) / "README.md").read_text())

    def test_compact_pr_hydration_and_exclusion(self):
        event = {
            "public": True,
            "repo": {"name": "owner/project"},
            "type": "PullRequestEvent",
            "created_at": "2026-09-10T00:00:00Z",
            "payload": {"action": "opened", "pull_request": {"number": 3}},
        }

        def fetch(endpoint):
            return {"title": "<fix> [link]"}

        rows = select_activity([[event]], fetch)
        self.assertEqual(rows[0]["url"], "https://github.com/owner/project/pull/3")
        ET.fromstring(render_activity(rows))
        self.assertIn("&#91;", markdown_activity(rows))
        event["repo"]["name"] = "jerome-queck/doomsday-protocol"
        self.assertEqual(select_activity([[event]], fetch), [])
        event["repo"]["name"] = "owner/project"
        event["public"] = False
        self.assertEqual(select_activity([[event]], fetch), [])

    def test_svg_escapes_text(self):
        root = ET.fromstring(render_counters((10, 8, 6), "<&>"))
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")

    def test_counter_layouts_share_values_timestamp_and_scope(self):
        for mobile, width in [(False, "900"), (True, "480")]:
            root = ET.fromstring(
                render_counters(
                    (1315, 1276, 966), "31 Oct 2026 15:45 UTC", mobile=mobile
                )
            )
            self.assertEqual(root.attrib["width"], width)
            copy = " ".join(root.itertext())
            for expected in [
                "1,315",
                "1,276",
                "966",
                "31 Oct 2026 15:45 UTC",
                "ALL TIME",
                "Linked issues resolved",
            ]:
                self.assertIn(expected, copy)

    def test_calendar_nonadvancing_cursors_fail_without_timeout(self):
        for cursor in (None, "repeated"):
            with self.subTest(cursor=cursor):

                def query(source, next_cursor=cursor, **variables):
                    if "commitContributionsByRepository" in source:
                        return {
                            "user": {
                                "contributionsCollection": {
                                    "totalRepositoriesWithContributedCommits": 0,
                                    "commitContributionsByRepository": [],
                                }
                            }
                        }
                    return {
                        "user": {
                            "contributionsCollection": {
                                "issueContributions": {
                                    "nodes": [],
                                    "pageInfo": {
                                        "hasNextPage": True,
                                        "endCursor": next_cursor,
                                    },
                                }
                            }
                        }
                    }

                with self.assertRaisesRegex(ValueError, "pagination did not advance"):
                    fetch_calendar(query, dt.date(2026, 11, 1))

    def test_calendar_legend_is_below_every_day_cell(self):
        for mobile in (False, True):
            root = ET.fromstring(
                render_calendar(dt.date(2025, 11, 2), dt.date(2026, 11, 1), {}, mobile)
            )
            cells = [
                node for node in root.iter() if node.tag.endswith("rect") and list(node)
            ]
            legend = [
                node
                for node in root.iter()
                if node.tag.endswith("rect") and node.get("width") == "23"
            ]
            bottom = max(
                float(node.get("y")) + float(node.get("height")) for node in cells
            )
            self.assertGreater(min(float(node.get("y")) for node in legend), bottom)

    def test_merge_months_zero_fills_and_bounds_dates(self):
        months = merge_months(
            {
                "2025-11-30": 10,
                "2025-12-01": 2,
                "2026-11-01": 3,
                "2026-11-02": 99,
                "2026-12-01": 99,
            },
            dt.date(2026, 11, 1),
        )
        self.assertEqual(len(months), 12)
        self.assertEqual(next(iter(months)), "2025-12")
        self.assertEqual(months["2026-01"], 0)
        self.assertEqual(months["2026-11"], 3)
        self.assertEqual(sum(months.values()), 5)

    def test_merge_dates_reuse_complete_public_pr_traversal(self):
        responses = [
            {"opened": {"issueCount": 10}, "merged": {"issueCount": 8}},
            {
                "user": {
                    "pullRequests": {
                        "nodes": [pr(), pr(private=True)],
                        "pageInfo": {"hasNextPage": True, "endCursor": "next"},
                    }
                }
            },
            {
                "user": {
                    "pullRequests": {
                        "nodes": [pr()],
                        "pageInfo": {"hasNextPage": False, "endCursor": None},
                    }
                }
            },
        ]
        with patch("scripts.profile_data.graphql", side_effect=responses) as query:
            result = fetch_contributions()
        self.assertEqual(result["counts"], [10, 8, 1])
        self.assertEqual(result["merged_dates"], {"2026-09-10": 2})
        self.assertEqual(query.call_args.kwargs, {"cursor": "next"})

    def test_nonadvancing_merged_pr_cursor_aborts(self):
        page = {
            "user": {
                "pullRequests": {
                    "nodes": [],
                    "pageInfo": {"hasNextPage": True, "endCursor": "same"},
                }
            }
        }
        with (
            patch(
                "scripts.profile_data.graphql",
                side_effect=[
                    {"opened": {"issueCount": 0}, "merged": {"issueCount": 0}},
                    page,
                    page,
                ],
            ),
            self.assertRaises(ValueError),
        ):
            fetch_contributions()

    def test_late_source_failure_leaves_previous_snapshot(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            patch(
                "scripts.profile_data.fetch_contributions",
                return_value={"counts": [10, 8, 6], "merged_dates": {}},
            ),
            patch(
                "scripts.profile_data.fetch_calendar",
                return_value=(dt.date(2026, 9, 10), {}),
            ),
            patch("scripts.profile_data.fetch_activity", return_value=[]),
            patch("scripts.profile_data.load_projects", return_value=[{}]),
            patch(
                "scripts.profile_data.fetch_repo_pulse",
                side_effect=RuntimeError("unavailable"),
            ),
            patch("sys.argv", ["profile_data", directory]),
        ):
            target = Path(directory) / "snapshot.json"
            target.write_text("previous")
            with self.assertRaises(RuntimeError):
                main()
            self.assertEqual(target.read_text(), "previous")
            self.assertEqual(list(Path(directory).iterdir()), [target])

    def test_all_graphics_and_text_derive_from_saved_snapshot(self):
        snapshot = {
            "schema_version": 1,
            "observed_from": "2026-11-01T00:00:00+00:00",
            "observed_to": "2026-11-01T00:01:00+00:00",
            "updated": "01 Nov 2026 00:01 UTC",
            "counts": [10, 8, 6],
            "calendar_start": "2025-11-02",
            "calendar_end": "2026-11-01",
            "calendar_days": {"2026-11-01": 3},
            "merge_months": merge_months({"2026-11-01": 2}, dt.date(2026, 11, 1)),
            "projects": [],
            "recent_events": [],
        }
        files = render_snapshot(snapshot)
        self.assertEqual(len(files), 11)
        self.assertEqual(files, render_snapshot(snapshot))
        for name, source in files.items():
            if name.endswith(".svg"):
                ET.fromstring(source)
                if name != "activity.svg":
                    self.assertIn(snapshot["updated"], source)
        self.assertIn("2026-11: 2", files["README.md"])
        self.assertIn('"2026-11": 2', files["snapshot.json"])

    def test_long_words_cannot_add_a_third_title_line(self):
        event = {
            "title": " ".join(["a" * 24] * 3),
            "repo": "owner/repo",
            "number": 1,
            "action": "opened",
            "date": "2026-10-31",
        }
        root = ET.fromstring(render_activity([event]))
        title_lines = [
            node for node in root.iter() if node.attrib.get("font-size") == "24"
        ]
        self.assertLessEqual(len(title_lines), 2)

    def test_remote_event_runs_have_declared_layout_widths(self):
        event = {
            "title": "W" * 80,
            "repo": "W" * 80,
            "number": 1,
            "action": "opened",
            "date": "2026-10-31",
        }
        root = ET.fromstring(render_activity([event]))
        runs = [
            node
            for node in root.iter()
            if node.attrib.get("font-size") == "24" or node.attrib.get("y") == "142"
        ]
        self.assertEqual(len(runs), 3)
        for node in runs:
            self.assertLessEqual(float(node.attrib["textLength"]), 576)
            self.assertEqual(node.attrib["lengthAdjust"], "spacingAndGlyphs")

    def test_recent_activity_stays_at_two_events(self):
        events = [
            {
                "public": True,
                "repo": {"name": "owner/project"},
                "type": "IssuesEvent",
                "created_at": "2026-10-31T00:00:00Z",
                "payload": {
                    "action": "opened",
                    "issue": {"number": n, "title": str(n)},
                },
            }
            for n in range(4)
        ]
        self.assertEqual([row["number"] for row in select_activity([events])], [0, 1])


if __name__ == "__main__":
    unittest.main()
