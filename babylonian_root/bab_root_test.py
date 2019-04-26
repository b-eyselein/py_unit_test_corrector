import unittest
from .bab_root import babylonian_square_root


class BabRootTest(unittest.TestCase):
    def test_bab_root(self):
        self.assertAlmostEqual(babylonian_square_root(2, 2), 1.416666666666665)
        self.assertAlmostEqual(babylonian_square_root(2., 6), 1.414213562373095)
        self.assertAlmostEqual(babylonian_square_root(42, 0), 42.)
        self.assertAlmostEqual(babylonian_square_root(4., 5), 2.)

        self.assertAlmostEqual(babylonian_square_root(2.25, 10), 1.5)

        self.assertAlmostEqual(babylonian_square_root(-4, 10), -2.0)

        with self.assertRaises(Exception):
            # number has to be int or float
            babylonian_square_root('', 1)

        with self.assertRaises(Exception):
            # rounds has to be an int
            babylonian_square_root(1, '')

        with self.assertRaises(Exception):
            # rounds must be greater or equal 0
            babylonian_square_root(1, -1)
