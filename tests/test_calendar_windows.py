import datetime as dt
import unittest
import xml.etree.ElementTree as ET
from collections import Counter

from scripts.profile_data import merge_months
from scripts.public_calendar import KINDS, _date_windows, fetch_calendar
from scripts.readme_world import _cadence


class CalendarWindowTests(unittest.TestCase):
    def test_inclusive_date_windows_cover_exact_year_leap_year_and_later_years(self):
        cases = [
            (dt.date(2026, 7, 1), dt.date(2027, 6, 30), [365]),
            (dt.date(2026, 7, 1), dt.date(2027, 7, 1), [365, 1]),
            (dt.date(2023, 7, 1), dt.date(2024, 6, 30), [365, 1]),
            (dt.date(2024, 2, 29), dt.date(2025, 3, 1), [365, 2]),
        ]
        for start, end, lengths in cases:
            with self.subTest(start=start, end=end):
                windows = list(_date_windows(start, end, 365))
                self.assertEqual([1 + (b - a).days for a, b in windows], lengths)
                covered = [
                    a + dt.timedelta(days=i)
                    for a, b in windows
                    for i in range(1 + (b - a).days)
                ]
                self.assertEqual(len(covered), (end - start).days + 1)
                self.assertEqual(len(covered), len(set(covered)))
                self.assertEqual((covered[0], covered[-1]), (start, end))

    def test_all_kinds_preserve_boundary_events_and_reset_pagination_each_year(self):
        dates = [
            "2026-07-01T00:00:00Z",
            "2027-06-30T23:59:59Z",
            "2027-07-01T00:00:00Z",
            "2027-07-02T23:59:59Z",
        ]
        connections = {
            "issueContributions": ("issues", "issue"),
            "pullRequestContributions": ("pull_requests", "pullRequest"),
            "pullRequestReviewContributions": ("reviews", None),
            "repositoryContributions": ("repositories", None),
        }
        calls = []

        def query(source, **variables):
            lower, upper = (
                dt.datetime.fromisoformat(variables[key].replace("Z", "+00:00"))
                for key in ("from", "to")
            )
            self.assertLess(upper - lower, dt.timedelta(days=365))
            selected = [
                date
                for date in dates
                if lower
                <= dt.datetime.fromisoformat(date.replace("Z", "+00:00"))
                <= upper
            ]
            commits = "commitContributionsByRepository" in source
            connection = (
                "commits"
                if commits
                else next(name for name in connections if name in source)
            )
            calls.append((connection, variables.copy()))
            kind, resource = ("commits", None) if commits else connections[connection]
            nodes = []
            for date in selected:
                identity = kind + date
                node = {
                    "isRestricted": False,
                    "occurredAt": date,
                    "repository": {"id": identity, "isPrivate": False},
                }
                if commits:
                    node["commitCount"] = 3
                elif resource:
                    node[resource] = {"id": identity, "repository": node["repository"]}
                elif kind == "reviews":
                    node["pullRequestReview"] = {"id": identity}
                nodes.append(node)
            if commits:
                value = {
                    "totalRepositoriesWithContributedCommits": len(nodes),
                    "commitContributionsByRepository": [
                        {
                            "contributions": {
                                "nodes": nodes,
                                "pageInfo": {"hasNextPage": False},
                            }
                        }
                    ],
                }
            else:
                offset = int(variables.get("cursor", "0"))
                more = offset + 1 < len(nodes)
                value = {
                    connection: {
                        "nodes": nodes[offset : offset + 1],
                        "pageInfo": {
                            "hasNextPage": more,
                            "endCursor": str(offset + 1) if more else None,
                        },
                    }
                }
            return {"user": {"contributionsCollection": value}}

        calendar = fetch_calendar(query, dt.date(2027, 7, 2))
        self.assertEqual(calendar.start, dt.date(2026, 7, 1))
        self.assertEqual(calendar.days, {date[:10]: 7 for date in dates})
        self.assertEqual(calendar.kinds, dict(zip(KINDS, [12, 4, 4, 4, 4])))
        for connection in connections:
            first_pages = [
                variables
                for name, variables in calls
                if name == connection and "cursor" not in variables
            ]
            self.assertEqual(
                [variables["from"] for variables in first_pages],
                ["2026-07-01T00:00:00Z", "2027-07-01T00:00:00Z"],
            )
            self.assertEqual(
                [variables["to"] for variables in first_pages],
                ["2027-06-30T23:59:59Z", "2027-07-02T23:59:59Z"],
            )

    def test_cadence_full_history_wraps_with_year_labels_and_bounded_ink(self):
        for today in (
            dt.date(2026, 11, 2),
            dt.date(2027, 6, 30),
            dt.date(2027, 12, 31),
            dt.date(2028, 7, 1),
        ):
            months = merge_months({}, today)
            months = {
                month: (100 if today.year == 2026 else 123456789) + i
                for i, month in enumerate(months)
            }
            for width, mobile, columns in ((480, True, 5), (900, False, 8)):
                with self.subTest(today=today, mobile=mobile):
                    document, end = _cadence(
                        {"merge_months": months, "calendar_end": str(today)},
                        width,
                        0,
                        mobile,
                    )
                    root = ET.fromstring("<svg>" + document + "</svg>")
                    labels = {
                        node.get("aria-label"): node
                        for node in root.iter()
                        if node.get("aria-label")
                    }
                    self.assertTrue(set(months).issubset(labels))
                    self.assertIn("2026-07", labels)
                    if today.year == 2026:
                        self.assertLess(end, 400)
                    else:
                        self.assertIn(
                            "2027-07"
                            if today.month == 7 and today.year == 2028
                            else "2027-06",
                            labels,
                        )
                    baselines = Counter(
                        labels[month].get("data-bounds").split()[1] for month in months
                    )
                    self.assertLessEqual(max(baselines.values()), columns)
                    boxes = []
                    for month, count in months.items():
                        for label in (month, str(count)):
                            node = labels[label]
                            bounds = [
                                float(value)
                                for value in node.get("data-bounds").split()
                            ]
                            x0, y0, x1, y1 = bounds
                            self.assertGreaterEqual(x0, 27)
                            self.assertLessEqual(x1, width - 27)
                            self.assertLess(y1, end)
                            boxes.append((x0, y0, x1, y1, label))
                    for i, a in enumerate(boxes):
                        for b in boxes[i + 1 :]:
                            self.assertFalse(
                                min(a[2], b[2]) > max(a[0], b[0])
                                and min(a[3], b[3]) > max(a[1], b[1]),
                                (a, b),
                            )
