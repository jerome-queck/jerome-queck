import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from scripts.profile_data import render_snapshot
from tests.test_snapshot_v2 import snapshot

ROOT = Path(__file__).resolve().parents[1]


class WorldTests(unittest.TestCase):
    def test_worlds_share_snapshot_numbers_and_timestamp(self):
        source = snapshot()
        source["counts"] = [127, 93, 41]
        files = render_snapshot(source)
        for name in (
            "world.svg",
            "world-mobile.svg",
            "world-still.svg",
            "world-mobile-still.svg",
        ):
            root = ET.fromstring(files[name])
            self.assertEqual(root.get("data-snapshot"), source["observed_to"])
            labels = {node.get("aria-label") for node in root.iter()}
            for value in ("127", "93", "41", "Collected " + source["updated"]):
                self.assertIn(value, labels)
            self.assertIn("2026-07-01 to 2026-11-02", labels)
            self.assertEqual(files[name], render_snapshot(source)[name])

    def test_data_room_carries_schema_three_values(self):
        from scripts.upstream_prs import change_footprint, open_pr_ages

        source = snapshot()
        doc = render_snapshot(source)["world-mobile.svg"]
        labels = {node.get("aria-label") for node in ET.fromstring(doc).iter()}
        for value in source["calendar_kinds"].values():
            self.assertTrue(
                any(label and label.startswith(f"{value:,}") for label in labels)
            )
        for item in source["upstream_prs"]:
            if item["state"] == "MERGED":
                self.assertTrue(
                    any(
                        label and "#" + str(item["number"]) in label for label in labels
                    )
                )
        footprint = change_footprint(source["upstream_prs"])
        for key in ("additions", "deletions", "file_changes"):
            self.assertIn(f"{footprint[key]:,}", labels)
        from collections import Counter

        ages = Counter(
            item["days"]
            for item in open_pr_ages(source["upstream_prs"], source["observed_to"])
        )
        for day in {0, 1, 2} | set(ages):
            self.assertIn(str(day) + " d", labels)
            self.assertIn(str(ages[day]), labels)

    def test_receipt_precedes_analytics_on_a_quiet_backing(self):
        for name in ("world.svg", "world-mobile.svg"):
            root = ET.fromstring(render_snapshot(snapshot())[name])
            nodes = list(root.iter())
            labels = {
                node.get("aria-label"): node
                for node in nodes
                if node.get("data-bounds")
            }
            receipt_y = float(
                labels["Open-source contributions"].get("data-bounds").split()[1]
            )
            analytics_y = float(
                labels["Public work / all time"].get("data-bounds").split()[1]
            )
            self.assertLess(receipt_y, analytics_y)
            self.assertFalse(
                any(node.tag.endswith(("image", "pattern")) for node in nodes)
            )

    def test_world_is_self_contained_opaque_and_ids_are_unique(self):
        for name, document in render_snapshot(snapshot()).items():
            if not name.startswith("world"):
                continue
            root = ET.fromstring(document)
            nodes = list(root.iter())
            ids = [node.get("id") for node in nodes if node.get("id")]
            self.assertEqual(len(ids), len(set(ids)))
            rectangles = [node for node in root if node.tag.endswith("rect")]
            self.assertEqual(rectangles[0].get("width"), root.get("width"))
            self.assertEqual(rectangles[0].get("height"), root.get("height"))
            self.assertNotIn("opacity", rectangles[0].attrib)
            for node in nodes:
                self.assertNotIn(
                    node.tag.split("}")[-1],
                    ("script", "foreignObject", "text"),
                )
                if node.get("href"):
                    href = node.get("href")
                    if href.startswith("#"):
                        self.assertIn(href[1:], ids)
                    else:
                        self.assertTrue(href.startswith("data:image/jpeg;base64,"))
            if "-still" in name:
                self.assertNotIn("<style>", document)
            for node in nodes:
                if node.tag.split("}")[-1] in ("animate", "animateTransform"):
                    self.fail("Motion must use reduced-motion-aware CSS")

    def test_root_readme_uses_native_links_for_projects_and_sources(self):
        from html.parser import HTMLParser

        from scripts.render_readme_world import PROJECTS

        class Links(HTMLParser):
            def __init__(self):
                super().__init__()
                self.hrefs = []

            def handle_starttag(self, tag, attrs):
                if tag == "a":
                    self.hrefs.append(dict(attrs).get("href"))

        readme = (ROOT / "README.md").read_text()
        links = Links()
        links.feed(readme)
        self.assertIn("Text edition, links and sources", readme)
        for _, name, description, repo, site in PROJECTS:
            self.assertIn("[" + name + "](", readme)
            self.assertIn(description, readme)
            self.assertIn(repo, links.hrefs)
            if site:
                self.assertIn(site, links.hrefs)
        self.assertIn("(prefers-reduced-motion: reduce)", readme)
        self.assertIn("## Open-source contributions", readme)
        for number in ("189784", "189855", "189960", "189993", "130275", "71474"):
            self.assertIn("/pull/" + number, readme)


if __name__ == "__main__":
    unittest.main()
