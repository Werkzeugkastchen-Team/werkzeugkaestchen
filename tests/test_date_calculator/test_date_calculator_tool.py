import pytest
from tools.date_calculator.date_calculator_tool import DateCalculatorTool

def test_valid_dates():
    """Test mit gültigen Daten"""
    tool = DateCalculatorTool()
    input_params = {
        'start_date': '01.01.2024',
        'end_date': '02.01.2024'
    }
    success = tool.execute_tool(input_params)
    assert success is True
    assert "Die Differenz beträgt <strong>1</strong> Tage." in tool.output
    assert not tool.error_message

def test_over_one_year():
    """Test mit gültigen Daten über ein Jahr"""
    tool = DateCalculatorTool()
    input_params = {
        'start_date': '01.01.2024',
        'end_date': '02.01.2025'
    }
    success = tool.execute_tool(input_params)
    assert success is True
    assert "367" in tool.output
    assert not tool.error_message

def test_invalid_format():
    """Test mit falschem Format"""
    tool = DateCalculatorTool()
    input_params = {
        'start_date': '2024-01-01',
        'end_date': '2024-01-02'
    }
    success = tool.execute_tool(input_params)
    assert success is False
    assert not tool.output
    assert tool.error_message == "Bitte geben Sie ein gültiges Datum im Format DD.MM.YYYY ein."

def test_invalid_year():
    """Test mit ungültigem Jahr"""
    tool = DateCalculatorTool()
    input_params = {
        'start_date': '01.01.1899',
        'end_date': '01.01.1900'
    }
    success = tool.execute_tool(input_params)
    assert success is False
    assert not tool.output
    assert tool.error_message == "Jahresangaben müssen ab 1900 sein."
