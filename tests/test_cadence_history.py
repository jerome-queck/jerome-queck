import datetime as dt
import unittest
import xml.etree.ElementTree as ET
from collections import Counter

from scripts.profile_data import merge_months, render_cadence, render_snapshot
from tests.test_snapshot_v2 import snapshot


class CadenceHistoryTests(unittest.TestCase):
    def test_desktop_large_counts_fit_their_month_columns(self):
        months = {
            month: 999999990 + i
            for i, month in enumerate(merge_months({}, dt.date(2027, 2, 1)))
        }
        root = ET.fromstring(render_cadence(months, "fixture"))
        labels = {
            node.get("aria-label"): node
            for node in root.iter()
            if node.get("aria-label")
        }
        for count in months.values():
            bounds = tuple(
                float(value) for value in labels[str(count)].get("data-bounds").split()
            )
            self.assertLessEqual(bounds[2] - bounds[0], 828 / 8 - 12)

    def test_every_payload_keeps_full_year_identified_history(self):
        previous_height = 0
        for today in (dt.date(2027, 6, 30), dt.date(2027, 12, 31), dt.date(2028, 7, 1)):
            with self.subTest(today=today):
                source = snapshot()
                source["calendar_end"] = str(today)
                source["observed_to"] = f"{today}T12:00:00+00:00"
                source["merge_months"] = {
                    month: 1500 + i for i, month in enumerate(merge_months({}, today))
                }
                files = render_snapshot(source)
                self.assertEqual(len(files), 15)
                for name, document in files.items():
                    if name.endswith(".svg"):
                        ET.fromstring(document)
                for name in ("cadence.svg", "cadence-mobile.svg"):
                    root = ET.fromstring(files[name])
                    width, height = float(root.get("width")), float(root.get("height"))
                    labels = {
                        node.get("aria-label"): node
                        for node in root.iter()
                        if node.get("aria-label")
                    }
                    self.assertTrue(set(source["merge_months"]).issubset(labels))
                    self.assertIn("2026-07", labels)
                    self.assertIn("+n = external project merges", labels)
                    self.assertIn("OPEN-SOURCE PR STATUS", labels)
                    boxes = []
                    for month, count in source["merge_months"].items():
                        for label in (month, str(count)):
                            bounds = tuple(
                                float(value)
                                for value in labels[label].get("data-bounds").split()
                            )
                            self.assertGreaterEqual(bounds[0], 0)
                            self.assertLessEqual(bounds[2], width)
                            self.assertLess(bounds[3], height)
                            boxes.append((*bounds, label))
                    for i, a in enumerate(boxes):
                        for b in boxes[i + 1 :]:
                            self.assertFalse(
                                min(a[2], b[2]) > max(a[0], b[0])
                                and min(a[3], b[3]) > max(a[1], b[1]),
                                (a, b),
                            )
                    if name == "cadence.svg":
                        self.assertGreater(height, previous_height)
                        previous_height = height
                        rows = Counter(
                            labels[month].get("data-bounds").split()[1]
                            for month in source["merge_months"]
                        )
                        self.assertLessEqual(max(rows.values()), 8)
                        last_month_bottom = max(
                            float(labels[month].get("data-bounds").split()[3])
                            for month in source["merge_months"]
                        )
                        status_top = float(
                            labels["+n = external project merges"]
                            .get("data-bounds")
                            .split()[1]
                        )
                        self.assertGreater(status_top, last_month_bottom)
