import unittest
from circle import Circle


class CircleTest(unittest.TestCase):
    def test_init(self):
        c1: Circle = Circle(1, 1, 1)
        self.assertEqual(1, c1.center_x)
        self.assertEqual(1, c1.center_y)
        self.assertEqual(1, c1.radius)

        c2: Circle = Circle(44, 55, 66)
        self.assertEqual(44, c2.center_x)
        self.assertEqual(55, c2.center_y)
        self.assertEqual(66, c2.radius)

        with self.assertRaises(Exception):
            Circle("str", 1, 1)

        with self.assertRaises(Exception):
            Circle(1, "str", 1)

        with self.assertRaises(Exception):
            Circle(1, 1, "str")

        with self.assertRaises(Exception):
            Circle(1, 1, -1)

    def test_area(self):
        self.assertAlmostEqual(3.141_592_653, Circle(0, 0, 1).area())
        self.assertAlmostEqual(12.566370614359172, Circle(0, 0, 2).area())


if __name__ == "__main__":
    unittest.main()
