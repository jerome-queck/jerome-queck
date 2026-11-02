import hashlib
import json
import re
import unittest
import xml.etree.ElementTree as ET

from scripts.profile_style import FONT_ROOT, measure, shaped, svg, text
from scripts.public_calendar import weekday_totals
from scripts.repo_pulse import language_bytes


class ProfileStyleTests(unittest.TestCase):
    def test_all_local_fonts_and_licenses_match_pinned_manifest(self):
        manifest = json.loads((FONT_ROOT / "manifest.json").read_text())
        self.assertEqual(
            {item["role"] for item in manifest}, {"display", "body", "mono"}
        )
        for item in manifest:
            self.assertRegex(item["revision"], r"^[a-f0-9]{40}$")
            for filename, digest in [
                (item["file"], item["sha256"]),
                (item["license"], item["license_sha256"]),
            ]:
                self.assertEqual(
                    hashlib.sha256((FONT_ROOT / filename).read_bytes()).hexdigest(),
                    digest,
                )
            self.assertIn(
                "SIL OPEN FONT LICENSE", (FONT_ROOT / item["license"]).read_text()
            )

    def test_shaped_ink_and_advance_fit_without_text_length(self):
        value = "AV e\u0301 ×"
        measured = measure(value, 40, "display")
        self.assertGreater(measured, 0)
        source = text(value, 28, 90, 40, "display", max_width=measured * 0.8)
        scale = float(re.search(r"scale\(([-.0-9]+)", source)[1])
        _, advance, bounds, _ = shaped(value, "display")
        self.assertLessEqual(
            (max(advance, bounds[2]) - min(0, bounds[0])) * scale,
            measured * 0.8 + 0.001,
        )
        document = svg(480, 120, source, "Actual <&> title")
        root = ET.fromstring(document)
        self.assertEqual(root[0].text, "Actual <&> title")
        self.assertEqual(len(list(root.iter("{http://www.w3.org/2000/svg}text"))), 0)
        self.assertNotIn("textLength", document)
        self.assertEqual(document, svg(480, 120, source, "Actual <&> title"))

    def test_unsupported_glyph_and_overflow_are_explicit_failures(self):
        with self.assertRaisesRegex(ValueError, "U\\+10FFFF"):
            text("\U0010ffff", 28, 90)
        with self.assertRaisesRegex(ValueError, "does not fit"):
            text("W" * 100, 28, 90, max_width=30)
        self.assertEqual(measure("", 24), 0)

    def test_weekday_frequency_uses_the_same_records(self):
        totals = weekday_totals({"2026-11-01": 7, "2026-11-02": 3, "2026-10-26": 4})
        self.assertEqual(totals["Sun"], 7)
        self.assertEqual(totals["Mon"], 7)
        self.assertEqual(sum(totals.values()), 14)

    def test_language_bytes_require_complete_matching_totals(self):
        empty = {
            "edges": [],
            "totalSize": 0,
            "totalCount": 0,
            "pageInfo": {"hasNextPage": False},
        }
        self.assertEqual(language_bytes(empty), {})
        for value in (
            None,
            {**empty, "totalSize": 1},
            {**empty, "totalCount": 1},
            {**empty, "pageInfo": {"hasNextPage": True}},
            {**empty, "totalSize": True},
        ):
            with self.assertRaises(ValueError):
                language_bytes(value)


if __name__ == "__main__":
    unittest.main()
