import unittest
from tools.date_calculator.date_calculator_tool import calculate_days_difference

class TestDateCalculatorTool(unittest.TestCase):
    def test_valid_dates(self):
        """Test mit gültigen Daten"""
        success, days, error = calculate_days_difference("01.01.2024", "02.01.2024")
        self.assertTrue(success)
        self.assertEqual(days, 1)
        self.assertIsNone(error)

    def test_invalid_format(self):
        """Test mit falschem Format"""
        success, days, error = calculate_days_difference("2024-01-01", "2024-01-02")
        self.assertFalse(success)
        self.assertIsNone(days)
        self.assertIsNotNone(error)

    def test_invalid_year(self):
        """Test mit ungültigem Jahr"""
        success, days, error = calculate_days_difference("01.01.1899", "01.01.1900")
        self.assertFalse(success)
        self.assertIsNone(days)
        self.assertIsNotNone(error)

if __name__ == '__main__':
    unittest.main() 