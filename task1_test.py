#!/usr/bin/env python
"""
    18/11/2023
    This does not need to be marked. These are my unit tests for task1, completely independent of the actual script.
"""

import unittest
import task1

class PrimeNumberTestCase(unittest.TestCase):
    """Tests for the 'is_prime' function."""

    def test_prime_numbers(self):
        prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        for number in prime_numbers:
            self.assertTrue(task1.is_prime(number), f"'{number}' is not recognized as a prime number.")

    def test_non_prime_numbers(self):
        non_prime_numbers = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
        for number in non_prime_numbers:
            self.assertFalse(task1.is_prime(number), f"'{number}' is falsely considered a prime number.")
            
if __name__ == '__main__': # Meant to be ran as an isolated script, outside of a module.
    unittest.main() # Run all tests.