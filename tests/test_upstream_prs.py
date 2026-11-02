import copy
import unittest

from scripts.upstream_prs import fetch_upstream, markdown_upstream, upstream_totals


def node(number=1, state="OPEN"):
    return {
        "id": f"PR{number}",
        "number": number,
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
        self.assertIn("天気", markdown_upstream(records, "now"))
        self.assertIn("&#91;fix&#93;", markdown_upstream(records, "now"))
        self.assertIn("CLOSED", markdown_upstream(records, "now"))

    def test_private_wrong_author_owned_or_state_mismatch_fail(self):
        mutations = [
            lambda n: n["repository"].update(isPrivate=True),
            lambda n: n["repository"].update(visibility="INTERNAL"),
            lambda n: n["author"].update(login="someone-else"),
            lambda n: n["repository"]["owner"].update(login="Jerome-Group"),
            lambda n: n.update(mergedAt="2026-11-01T00:00:00Z"),
            lambda n: n.update(closedAt="2026-11-01T00:00:00Z"),
            lambda n: n.update(createdAt="not-a-date"),
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
