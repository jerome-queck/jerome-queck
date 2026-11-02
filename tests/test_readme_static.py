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

    def test_mobile_descriptions_fit_at_least_23_source_pixels(self):
        import re
        from textwrap import wrap

        from scripts.profile_style import face

        root = ET.parse(ART / "full-mobile-still.svg").getroot()
        groups = [n for n in root.iter() if n.get("data-bounds")]
        units = face("body")[0]["head"].unitsPerEm
        for index, (_, _, description, _, _) in enumerate(PROJECTS):
            top = (index + 1) * 220
            for line in wrap(description, 19):
                matches = [
                    n
                    for n in groups
                    if n.get("aria-label") == line
                    and top <= float(n.get("data-bounds").split()[1]) < top + 220
                ]
                self.assertEqual(len(matches), 1, line)
                node = matches[0]
                bounds = list(map(float, node.get("data-bounds").split()))
                self.assertLess(bounds[3], top + 200)
                transform = next(child for child in node if child.get("transform")).get(
                    "transform"
                )
                scale = float(re.search(r"scale\(([-.0-9]+)", transform).group(1))
                self.assertGreaterEqual(scale * units, 22.99)

    def test_still_masters_have_no_animation(self):
        for size in ("wide", "mobile"):
            for role in ("full", "title", "source"):
                data = (ART / f"{role}-{size}-still.svg").read_text()
                self.assertNotIn("<style>", data)
                self.assertNotIn("<animate", data)


if __name__ == "__main__":
    unittest.main()
