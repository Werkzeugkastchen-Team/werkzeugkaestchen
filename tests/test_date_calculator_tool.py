import pytest
from tools.date_calculator.date_calculator_tool import calculate_days_difference

def test_valid_dates():
    """Test mit gültigen Daten"""
    success, days, error = calculate_days_difference("01.01.2024", "02.01.2024")
    assert success is True
    assert days == 1
    assert error is None

def test_invalid_format():
    """Test mit falschem Format"""
    success, days, error = calculate_days_difference("2024-01-01", "2024-01-02")
    assert success is False
    assert days is None
    assert error == "Bitte geben Sie ein gültiges Datum im Format DD.MM.YYYY ein."

def test_invalid_year():
    """Test mit ungültigem Jahr"""
    success, days, error = calculate_days_difference("01.01.1899", "01.01.1900")
    assert success is False
    assert days is None
    assert error == "Jahresangaben müssen ab 1900 sein."