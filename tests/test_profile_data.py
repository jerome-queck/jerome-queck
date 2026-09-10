import unittest
import xml.etree.ElementTree as ET

from scripts.profile_data import public_calendar_check, render_counters, resolved_issues


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

    def test_private_calendar_fails(self):
        with self.assertRaises(ValueError):
            public_calendar_check(
                {
                    "restrictedContributionsCount": 1,
                    "hasAnyRestrictedContributions": True,
                }
            )

    def test_svg_escapes_text(self):
        root = ET.fromstring(render_counters((10, 8, 6), "<&>"))
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")


if __name__ == "__main__":
    unittest.main()
