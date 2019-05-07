import unittest

from factorial_0 import factorial


class FactorialTest(unittest.TestCase):
    def test_factorial(self):
        self.assertEqual(1, factorial(0))
        self.assertEqual(1, factorial(1))
        self.assertEqual(3628800, factorial(10))
        self.assertEqual(15511210043330985984000000, factorial(25))

        with self.assertRaises(Exception):
            factorial('0.5')

        with self.assertRaises(Exception):
            factorial(-1)


if __name__ == "__main__":
    unittest.main()
