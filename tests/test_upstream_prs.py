import copy
import json
import unittest
from pathlib import Path

from scripts.upstream_prs import (
    change_footprint,
    fetch_upstream,
    markdown_upstream,
    open_pr_ages,
    upstream_totals,
)


def node(number=1, state="OPEN"):
    return {
        "id": f"PR{number}",
        "number": number,
        "additions": 12,
        "deletions": 3,
        "changedFiles": 2,
        "title": "Unicode e\u0301 天気 [fix]",
        "url": f"https://github.com/upstream/project/pull/{number}",
        "state": state,
        "createdAt": "2026-10-01T00:00:00Z",
        "updatedAt": "2026-11-01T00:00:00Z",
        "closedAt": None if state == "OPEN" else "2026-11-01T00:00:00Z",
        "mergedAt": "2026-11-01T00:00:00Z" if state == "MERGED" else None,
        "merge_commit_sha": "NOT_EVIDENCE_OF_MERGE",
        "author": {"login": "jerome-queck"},
        "repository": {
            "nameWithOwner": "upstream/project",
            "owner": {"login": "upstream"},
            "isPrivate": False,
            "visibility": "PUBLIC",
        },
    }


def page(nodes, count=None, cursor=None):
    return {
        "search": {
            "issueCount": len(nodes) if count is None else count,
            "nodes": nodes,
            "pageInfo": {"hasNextPage": cursor is not None, "endCursor": cursor},
        }
    }


class UpstreamTests(unittest.TestCase):
    def test_complete_public_fixture_readback(self):
        source = json.loads(
            (Path(__file__).parent / "fixtures/public-metrics-v3.json").read_text()
        )
        records = source["upstream_prs"]
        self.assertEqual(len(records), 18)
        self.assertEqual(upstream_totals(records), (6, 11, 3))
        self.assertEqual(
            change_footprint(records),
            {"prs": 6, "additions": 753, "deletions": 264, "file_changes": 96},
        )
        ages = open_pr_ages(records, source["observed_to"])
        self.assertEqual([row["days"] for row in ages], [2] + [1] * 9 + [0])
        self.assertEqual(sum(source["calendar_days"].values()), 4336)
        self.assertEqual(
            source["calendar_kinds"],
            {
                "commits": 1650,
                "issues": 1346,
                "pull_requests": 1314,
                "reviews": 11,
                "repositories": 15,
            },
        )
        self.assertEqual(
            sum(source["calendar_kinds"].values()),
            sum(source["calendar_days"].values()),
        )
        native = markdown_upstream(records, source["observed_to"])
        self.assertTrue(all(row["url"] in native for row in records))

    def test_complete_pagination_states_and_native_unicode(self):
        pages = [
            page([node()], 3, "next"),
            page([node(2, "MERGED"), node(3, "CLOSED")], 3),
        ]
        calls = []

        def query(source, **variables):
            calls.append(variables)
            return pages[len(calls) - 1]

        records = fetch_upstream(query)
        self.assertEqual(upstream_totals(records), (1, 1, 1))
        self.assertEqual(calls[1]["cursor"], "next")
        self.assertIn("-user:jerome-queck -org:Jerome-Group", calls[0]["search"])
        self.assertIsNone(records[0]["merged_at"])
        self.assertIn("天気", markdown_upstream(records, "2026-11-02T00:00:00Z"))
        self.assertIn(
            "&#91;fix&#93;", markdown_upstream(records, "2026-11-02T00:00:00Z")
        )
        self.assertIn("CLOSED", markdown_upstream(records, "2026-11-02T00:00:00Z"))

    def test_footprint_only_merged_patch_statistics(self):
        records = fetch_upstream(
            lambda *a, **kw: page([node(), node(2, "MERGED"), node(3, "CLOSED")])
        )
        self.assertEqual(
            change_footprint(records),
            {"prs": 1, "additions": 12, "deletions": 3, "file_changes": 2},
        )
        for field in ("additions", "deletions", "changed_files"):
            for invalid in (-1, True, None):
                broken = copy.deepcopy(records)
                broken[1][field] = invalid
                with self.assertRaises(ValueError):
                    change_footprint(broken)
        self.assertEqual(
            change_footprint([]),
            {"prs": 0, "additions": 0, "deletions": 0, "file_changes": 0},
        )

    def test_open_age_uses_observation_and_completed_utc_periods(self):
        records = fetch_upstream(
            lambda *a, **kw: page([node(), node(2, "MERGED"), node(3, "CLOSED")])
        )
        result = open_pr_ages(records, "2026-11-02T23:59:59Z")
        self.assertEqual(
            result,
            [
                {
                    "repo": "upstream/project",
                    "number": 1,
                    "url": "https://github.com/upstream/project/pull/1",
                    "days": 32,
                }
            ],
        )
        self.assertEqual(open_pr_ages(records, "2026-11-03T00:00:00Z")[0]["days"], 33)
        for observed in ("2026-09-30T00:00:00Z", "2026-10-02T00:00:00Z", "2026-11-03"):
            with self.assertRaises(ValueError):
                open_pr_ages(records, observed)
        records[0]["closed_at"] = "2026-11-01T00:00:00Z"
        with self.assertRaises(ValueError):
            open_pr_ages(records, "2026-11-03T00:00:00Z")

    def test_missing_negative_and_boolean_patch_fields_fail(self):
        for field in ("additions", "deletions", "changedFiles"):
            for invalid in (-1, True, None):
                item = node()
                item[field] = invalid
                with self.assertRaises(ValueError):
                    fetch_upstream(lambda *a, item=item, **kw: page([item]))

    def test_private_wrong_author_owned_or_state_mismatch_fail(self):
        mutations = [
            lambda n: n["repository"].update(isPrivate=True),
            lambda n: n["repository"].update(visibility="INTERNAL"),
            lambda n: n["author"].update(login="someone-else"),
            lambda n: n["repository"]["owner"].update(login="Jerome-Group"),
            lambda n: n.update(mergedAt="2026-11-01T00:00:00Z"),
            lambda n: n.update(closedAt="2026-11-01T00:00:00Z"),
            lambda n: n.update(createdAt="not-a-date"),
            lambda n: n.update(createdAt="2026-11-02T00:00:00Z"),
            lambda n: n.update(updatedAt="2026-09-01T00:00:00Z"),
        ]
        for mutate in mutations:
            record = node()
            record["title"] = "PRIVATE_CANARY"
            mutate(record)
            with self.assertRaises(ValueError) as error:
                fetch_upstream(lambda *a, record=record, **kw: page([record]))
            self.assertNotIn("PRIVATE_CANARY", str(error.exception))

    def test_empty_is_valid_but_partial_or_unbounded_search_fails(self):
        self.assertEqual(fetch_upstream(lambda *a, **kw: page([])), [])
        for response in (
            page([], 1),
            page([node()], 1001),
            page([], True),
            page([], 1, "next"),
        ):
            with self.assertRaises(ValueError):
                fetch_upstream(lambda *a, response=response, **kw: response)
        for pages in (
            [page([node()], 2, "next"), page([node()], 2)],
            [page([node()], 2, "next"), page([node(2)], 3)],
            [page([node()], 3, "same"), page([node(2)], 3, "same")],
        ):
            pending = iter(copy.deepcopy(pages))
            with self.assertRaises(ValueError):
                fetch_upstream(lambda *a, pending=pending, **kw: next(pending))


if __name__ == "__main__":
    unittest.main()
