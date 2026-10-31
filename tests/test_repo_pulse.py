import copy
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from scripts.repo_pulse import (
    fetch_repo_pulse,
    load_projects,
    markdown_pulse,
    render_pulse,
)

ROOT = Path(__file__).resolve().parents[1]


def release(tag, published, url, draft=False, prerelease=False):
    return {
        "tagName": tag,
        "publishedAt": published,
        "url": url,
        "isDraft": draft,
        "isPrerelease": prerelease,
    }


def page(releases=(), next_cursor=None):
    return {
        "repository": {
            "nameWithOwner": "Jerome-Group/algebra",
            "visibility": "PUBLIC",
            "isPrivate": False,
            "isEmpty": False,
            "url": "https://github.com/Jerome-Group/algebra",
            "defaultBranchRef": {
                "name": "trunk",
                "target": {
                    "__typename": "Commit",
                    "oid": "abc",
                    "committedDate": "2026-01-02T00:00:00Z",
                    "url": "https://github.com/Jerome-Group/algebra/commit/abc",
                },
            },
            "releases": {
                "nodes": list(releases),
                "pageInfo": {
                    "hasNextPage": next_cursor is not None,
                    "endCursor": next_cursor,
                },
            },
        }
    }


class RepoPulseTests(unittest.TestCase):
    def setUp(self):
        self.projects = load_projects(ROOT / "data/projects.json")
        self.project = self.projects[0]

    def test_catalogue_and_invalid_variants(self):
        self.assertEqual(len(self.projects), 9)
        self.assertEqual(self.projects[0]["summary"], "Structure and symmetry.")
        for invalid in (
            "Jerome-Group/clarifold",
            "other/algebra",
            "Jerome-Group/a/b",
            self.projects[1]["repo"],
        ):
            projects = copy.deepcopy(list(self.projects))
            projects[0]["repo"] = invalid
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "projects.json"
                path.write_text(json.dumps(projects))
                with self.assertRaises(ValueError):
                    load_projects(path)

    def test_public_guard_does_not_expose_private_data(self):
        for field, value in (
            ("isPrivate", True),
            ("visibility", "INTERNAL"),
            ("nameWithOwner", "other/repo"),
        ):
            response = page()
            response["repository"][field] = value
            response["repository"]["defaultBranchRef"]["target"]["oid"] = (
                "SECRET_CANARY"
            )
            with self.assertRaises(ValueError) as error:
                fetch_repo_pulse(
                    lambda *args, response=response, **kwargs: response, self.project
                )
            self.assertNotIn("SECRET_CANARY", str(error.exception))
        with self.assertRaises(ValueError):
            fetch_repo_pulse(lambda *args, **kwargs: {"repository": None}, self.project)

    def test_release_pagination_publication_date_and_tie(self):
        pages = [
            page(
                [
                    release("old", "2026-01-03T00:00:00Z", "https://example/a"),
                    release(
                        "draft", "2028-01-01T00:00:00Z", "https://example/d", draft=True
                    ),
                ],
                "next",
            ),
            page(
                [
                    release("new", "2027-01-01T00:00:00Z", "https://example/a"),
                    release(
                        "rc<&",
                        "2027-01-01T00:00:00Z",
                        "https://example/z",
                        prerelease=True,
                    ),
                ]
            ),
        ]
        calls = []

        def graphql(query, **variables):
            calls.append(variables)
            return pages[len(calls) - 1]

        result = fetch_repo_pulse(graphql, self.project)
        self.assertEqual(calls[1]["cursor"], "next")
        self.assertEqual(result["release"]["tag"], "rc<&")
        self.assertTrue(result["release"]["prerelease"])
        self.assertEqual(result["default_branch"], "trunk")
        self.assertEqual(result["head"]["oid"], "abc")
        self.assertIsNone(
            fetch_repo_pulse(
                lambda *args, **kwargs: page([release("draft", None, "x", draft=True)]),
                self.project,
            )["release"]
        )
        for mobile in (False, True):
            root = ET.fromstring(render_pulse((result,), "Updated now", mobile))
            content = " ".join(root.itertext())
            self.assertIn("rc<&", content)
            self.assertIn("2026-01-02", content)
            self.assertIn("prerelease", content)
        self.assertIn("rc\\<&", markdown_pulse((result,)))

    def test_incomplete_pages_and_empty_repository(self):
        with self.assertRaises(ValueError):
            fetch_repo_pulse(
                lambda *args, **kwargs: page(next_cursor="same"), self.project
            )
        bad = page(next_cursor="next")
        bad["repository"]["releases"]["pageInfo"]["endCursor"] = None
        with self.assertRaises(ValueError):
            fetch_repo_pulse(lambda *args, **kwargs: bad, self.project)
        empty = page()
        empty["repository"].update(isEmpty=True, defaultBranchRef=None)
        self.assertIsNone(
            fetch_repo_pulse(lambda *args, **kwargs: empty, self.project)["head"]
        )
        empty["repository"]["isEmpty"] = False
        with self.assertRaises(ValueError):
            fetch_repo_pulse(lambda *args, **kwargs: empty, self.project)


if __name__ == "__main__":
    unittest.main()
