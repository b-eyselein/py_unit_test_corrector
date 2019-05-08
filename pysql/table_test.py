import unittest
from table import *


class TableTest(unittest.TestCase):

    def testInsert(self):
        raum = Table('raum')
        raum.load_from_csv('raum.csv')

        raum2 = Table('raum2')
        raum2.copy(raum)

        with self.assertRaises(Exception):
            raum.insert(['info_turing', 'turing'])

        with self.assertRaises(Exception):
            raum.insert(['500', 'turing', 500])

        row = ['info_turing', 'turing', 500]
        self.assertTrue(raum.insert(row))

        self.assertEqual(len(raum.data), len(raum2.data) + 1)
        self.assertEqual(len(raum.data[0]), len(raum2.data[0]))

        self.assertListEqual(raum.data[-1], row)
        self.assertListEqual(raum2.data, raum.data[:-1])

        raum.insert(['info_zuse', 'zuse', '500'])
        self.assertListEqual(raum.data[-1], ['info_zuse', 'zuse', 500.0])


if __name__ == "__main__":
    unittest.main()
