import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from scripts.render_readme_world import PROJECTS

ART = Path(__file__).resolve().parents[1] / "assets/pixel-world"


class LinkedRooms(unittest.TestCase):
    def test_every_project_has_a_native_view_in_each_master(self):
        for size in ("wide", "mobile"):
            for role in ("full", "title", "source"):
                for motion in ("still", "ambient"):
                    root = ET.parse(ART / f"{role}-{size}-{motion}.svg").getroot()
                    views = {n.get("id") for n in root.iter() if n.tag.endswith("view")}
                    self.assertTrue({row[0] for row in PROJECTS} <= views)
                    self.assertIn("hero", views)

    def test_narrow_source_hit_area_meets_48_pixels(self):
        root = ET.parse(ART / "source-mobile-still.svg").getroot()
        self.assertGreaterEqual(int(root.get("height")) * 293 / 480, 48)

    def test_still_masters_have_no_animation(self):
        for size in ("wide", "mobile"):
            for role in ("full", "title", "source"):
                data = (ART / f"{role}-{size}-still.svg").read_text()
                self.assertNotIn("<style>", data)
                self.assertNotIn("<animate", data)


if __name__ == "__main__":
    unittest.main()
