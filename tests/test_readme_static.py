import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from scripts.render_readme_world import PROJECTS, load_room_projects

ART = Path(__file__).resolve().parents[1] / "assets/pixel-world"


class CanonicalRooms(unittest.TestCase):
    def test_catalogue_names_and_urls_reach_rooms_without_changing_captions(self):
        path = ART.parents[1] / "data/projects.json"
        catalogue = json.loads(path.read_text())
        algebra = next(
            row for row in catalogue if row["repo"] == "Jerome-Group/algebra"
        )
        algebra["name"] = "Algebra renamed"
        algebra["url"] = "https://algebra.example.org/notes"
        algebra["summary"] = "A longer native description."
        catalogue.reverse()
        with tempfile.TemporaryDirectory() as directory:
            changed = Path(directory) / "projects.json"
            changed.write_text(json.dumps(catalogue))
            rooms = load_room_projects(changed)
        self.assertEqual(
            [row[0] for row in rooms],
            [
                "ntulearn",
                "academic-os",
                "syrax",
                "emmy",
                "algebra",
                "calculus",
                "probability",
                "numbertheory",
                "calculator",
            ],
        )
        self.assertEqual(
            next(row for row in rooms if row[0] == "algebra"),
            (
                "algebra",
                "Algebra renamed",
                "Structure, symmetry and proofs.",
                "https://github.com/Jerome-Group/algebra",
                "https://algebra.example.org/notes",
            ),
        )
        self.assertEqual(len(rooms), len(catalogue))
        self.assertEqual(
            {row[3] for row in rooms},
            {f"https://github.com/{row['repo']}" for row in catalogue},
        )
        self.assertTrue(all(row[4] is None for row in rooms[:4]))
        self.assertTrue(all(row[4] is not None for row in rooms[4:]))

    def test_catalogue_selection_change_requires_deliberate_room_update(self):
        catalogue = json.loads((ART.parents[1] / "data/projects.json").read_text())
        for replacement in ("another-project", "clarifold", "doomsday-protocol"):
            with (
                self.subTest(replacement=replacement),
                tempfile.TemporaryDirectory() as directory,
            ):
                catalogue[0]["repo"] = f"Jerome-Group/{replacement}"
                changed = Path(directory) / "projects.json"
                changed.write_text(json.dumps(catalogue))
                with self.assertRaises(ValueError):
                    load_room_projects(changed)


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
            top = (index + 1) * 155
            line_length = 17 if index in (2, 3) else 23
            self.assertLessEqual(len(wrap(description, line_length)), 2)
            for line in wrap(description, line_length):
                matches = [
                    n
                    for n in groups
                    if n.get("aria-label") == line
                    and top <= float(n.get("data-bounds").split()[1]) < top + 155
                ]
                self.assertEqual(len(matches), 1, line)
                node = matches[0]
                bounds = list(map(float, node.get("data-bounds").split()))
                self.assertLess(bounds[3], top + 142)
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
