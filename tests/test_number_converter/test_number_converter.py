import pytest
from tools.number_converter.number_converter_tool import NumberConverterTool

def test_number_converter_initialization():
    """Test if the tool initializes correctly"""
    tool = NumberConverterTool()
    assert tool.name == "Zahlenkonverter"
    assert "number" in tool.input_params
    assert "input_type" in tool.input_params

def test_binary_conversion():
    """Test binary number conversion"""
    tool = NumberConverterTool()
    result = tool.execute_tool({"number": "1010", "input_type": "binary"})
    assert result == True
    assert "10" in tool.output  # Decimal
    assert "A" in tool.output.upper()  # Hex

def test_decimal_conversion():
    """Test decimal number conversion"""
    tool = NumberConverterTool()
    result = tool.execute_tool({"number": "42", "input_type": "decimal"})
    assert result == True
    assert "101010" in tool.output  # Binary
    assert "2A" in tool.output.upper()  # Hex

def test_hexadecimal_conversion():
    """Test hexadecimal number conversion"""
    tool = NumberConverterTool()
    result = tool.execute_tool({"number": "2A", "input_type": "hexadecimal"})
    assert result == True
    assert "42" in tool.output  # Decimal
    assert "101010" in tool.output  # Binary

def test_invalid_input():
    """Test handling of invalid input"""
    tool = NumberConverterTool()
    result = tool.execute_tool({"number": "XYZ", "input_type": "binary"})
    assert result == False
    assert "Ungültige Eingabe" in tool.error_message

def test_empty_input():
    """Test handling of empty input"""
    tool = NumberConverterTool()
    result = tool.execute_tool({"number": "", "input_type": "decimal"})
    assert result == False
    assert "Bitte geben Sie eine Zahl" in tool.error_message 