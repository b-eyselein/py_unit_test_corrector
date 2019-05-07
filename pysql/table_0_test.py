import unittest
import numpy as np
from table_0 import *


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
        self.assertListEqual(raum.data[-1], row)
        old_shape = list(np.shape(raum2.data))
        old_shape[0] += 1
        self.assertEqual(list(np.shape(raum.data)), old_shape)
        self.assertListEqual(raum2.data, raum.data[:-1])
        row = ['info_zuse', 'zuse', '500']
        self.assertTrue(raum.insert(row))


if __name__ == "__main__":
    unittest.main()
