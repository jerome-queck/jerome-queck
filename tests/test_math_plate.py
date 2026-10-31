import unittest

from scripts.render_math_plate import START, reflect, rotate, route_points


class MathPlateTests(unittest.TestCase):
    def test_the_order_changes_the_marked_corner(self):
        self.assertEqual(route_points("RS"), [(1, 1), (-1, 1), (-1, -1)])
        self.assertEqual(route_points("SR"), [(1, 1), (1, -1), (1, 1)])

    def test_operations_preserve_the_square_and_close_at_the_expected_order(self):
        corners = {(1, 1), (-1, 1), (-1, -1), (1, -1)}
        self.assertEqual({rotate(point) for point in corners}, corners)
        self.assertEqual({reflect(point) for point in corners}, corners)
        self.assertEqual(route_points("RRRR")[-1], START)
        self.assertEqual(route_points("SS")[-1], START)


if __name__ == "__main__":
    unittest.main()
