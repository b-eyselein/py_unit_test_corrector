import unittest
from table import *


class TableTest(unittest.TestCase):

    def testInsert(self):
        raum = Table('raum')
        raum.load_from_csv('raum.csv')
        raum2 = Table('raum2')
        raum2.copy(raum)
        row = ['info_turing', 'turing']
        self.assertFalse(raum.insert(row))
        row = ['500', 'turing', 500]
        self.assertFalse(raum.insert(row))
        row = ['info_turing', 'turing', 500]
        self.assertTrue(raum.insert(row))
        self.assertListEqual(raum.data[2], row)
        self.assertEqual(len(raum.data), len(raum2.data)+1)
        self.assertListEqual(raum2.data, raum.data[:-1])
        row = ['info_zuse', 'zuse', '500']
        self.assertTrue(raum.insert(row))


if __name__ == "__main__":
    unittest.main()
