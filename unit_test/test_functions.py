import unittest
from functions import *

class TestFunctions(unittest.TestCase):
    
    def test_add(self):
        self.assertEqual(add(3, 7), 10)
        self.assertEqual(add(-3, 7), 4)
        self.assertEqual(add(-3, -7), -10)
        self.assertEqual(add(1, -1), 0)
        
    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(11, 4), 2.75)
        self.assertEqual(divide(-11, 4), -2.75)
        self.assertEqual(divide(8, -5), -1.6)
        self.assertEqual(divide(-11, -4), 2.75)
        self.assertRaises(ValueError, divide, 5, 0)
        
    def test_power(self):
        self.assertEqual(power(2,10), 1024)
        self.assertEqual(power(-2,10), 1024)
        self.assertEqual(power(-2,9), -512)
        self.assertEqual(power(2,0), 1)
        self.assertEqual(power(9.31231, 0), 1)
        self.assertEqual(power(0, 6), 0)
        with self.assertRaises(ValueError):
            power(0, -6.4353)
        with self.assertRaises(ValueError):
            power(0, 0)
        
    
if __name__ == "__main__":
    unittest.main()        
        
