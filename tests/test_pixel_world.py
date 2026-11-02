import unittest
from xml.etree import ElementTree as ET

from scripts.pixel_world import PALETTE, SCENE_SIZE, render_scene


class PixelWorldTest(unittest.TestCase):
    def test_variants_are_deterministic_bounded_svg(self):
        for mobile, key in ((False, "wide"), (True, "mobile")):
            for motion in ("none", "ambient", "character"):
                svg = render_scene(mobile, motion)
                self.assertEqual(svg, render_scene(mobile, motion))
                root = ET.fromstring(svg)
                self.assertEqual(
                    (int(root.get("width")), int(root.get("height"))), SCENE_SIZE[key]
                )
                self.assertLess(len(svg.encode()), 250_000)
                self.assertIn("A tiny midnight workshop", svg)
                self.assertNotIn(
                    "http://", svg.replace("http://www.w3.org/2000/svg", "")
                )

    def test_motion_is_decorative_and_respects_reduced_motion(self):
        static = ET.fromstring(render_scene(motion="none"))
        for mode in ("ambient", "character"):
            svg = render_scene(motion=mode)
            self.assertIn("prefers-reduced-motion:reduce", svg)
            root = ET.fromstring(svg)
            # The complete painted world is identical across motion choices.
            paths = lambda node: [
                ET.tostring(e) for e in node if e.tag.endswith("path")
            ]
            self.assertEqual(paths(static), paths(root))
        self.assertEqual(PALETTE["ink"], "#f4dfb5")
        with self.assertRaises(ValueError):
            render_scene(motion="unknown")


if __name__ == "__main__":
    unittest.main()
