import unittest

from ggt_0 import ggt


class GgtTest(unittest.TestCase):
    def test_ggt(self):
        self.assertEqual(2, ggt(2, 2))
        self.assertEqual(1, ggt(2, 3))
        self.assertEqual(11, ggt(11, 77))
        self.assertEqual(5, ggt(25, 95))
        self.assertEqual(1, ggt(664, 337))

        with self.assertRaises(Exception):
            ggt('1', 1)

        with self.assertRaises(Exception):
            ggt(1, '1')

        with self.assertRaises(Exception):
            ggt(-1, 1)

        with self.assertRaises(Exception):
            ggt(1, -1)


if __name__ == "__main__":
    unittest.main()
