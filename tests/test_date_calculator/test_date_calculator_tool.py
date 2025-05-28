import pytest
from tools.date_calculator.date_calculator_tool import DateCalculatorTool
from flask_babel import lazy_gettext as _

def test_valid_dates():
    """Test mit gültigen Daten"""
    tool = DateCalculatorTool()
    input_params = {
        _('Startdatum'): '01.01.2024',
        _('Enddatum'): '02.01.2024'
    }
    success = tool.execute_tool(input_params)
    assert success is True
    assert "Die Differenz beträgt <strong>1</strong> Tage." in tool.output
    assert not tool.error_message

def test_over_one_year():
    """Test mit gültigen Daten über ein Jahr"""
    tool = DateCalculatorTool()
    input_params = {
        _('Startdatum'): '01.01.2024',
        _('Enddatum'): '02.01.2025'
    }
    success = tool.execute_tool(input_params)
    assert success is True
    assert "367" in tool.output
    assert not tool.error_message

def test_invalid_format():
    """Test mit falschem Format"""
    tool = DateCalculatorTool()
    input_params = {
        _('Startdatum'): 'something',
        _('Enddatum'): 'lala'
    }
    success = tool.execute_tool(input_params)
    assert success is False
    assert not tool.output
    assert tool.error_message == _("Bitte geben Sie ein gültiges Datum im Format TT.MM.JJJJ oder YYYY-MM-DD ein.")

def test_invalid_year():
    """Test mit ungültigem Jahr"""
    tool = DateCalculatorTool()
    input_params = {
        _('Startdatum'): '01.01.1899',
        _('Enddatum'): '01.01.1900'
    }
    success = tool.execute_tool(input_params)
    assert success is False
    assert not tool.output
    assert tool.error_message == "Jahresangaben müssen ab 1900 sein."
