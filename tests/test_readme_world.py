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
                    ("script", "image", "foreignObject", "text"),
                )
                if node.get("href"):
                    self.assertTrue(node.get("href").startswith("#"))
                    self.assertIn(node.get("href")[1:], ids)
            if "-still" in name:
                self.assertNotIn("<style>", document)
            else:
                self.assertIn("prefers-reduced-motion", document)
            for node in nodes:
                if node.tag.split("}")[-1] in ("animate", "animateTransform"):
                    self.fail("Motion must use reduced-motion-aware CSS")

    def test_root_readme_uses_single_world_picture_and_native_destinations(self):
        readme = (ROOT / "README.md").read_text()
        self.assertEqual(readme.count("<picture>"), 1)
        self.assertIn("world-mobile.svg", readme)
        self.assertIn("world.svg", readme)
        self.assertIn("Contributions merged into OpenClaw and freeCodeCamp", readme)
        self.assertIn("open proposals", readme)
        for repo in (
            "algebra",
            "calculus",
            "probability",
            "numbertheory",
            "calculator",
            "ntulearn",
            "academic-os",
            "syrax",
            "emmy",
        ):
            self.assertIn("/" + repo + ")", readme)


if __name__ == "__main__":
    unittest.main()
