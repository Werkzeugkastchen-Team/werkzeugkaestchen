import pytest
from tools.random_number_generator.random_number_generator_tool import RandomNumberGeneratorTool
import sys

def test_random_number_generator_initialization():
    """Test if the tool initializes correctly"""
    tool = RandomNumberGeneratorTool()
    assert tool.name == "Zufallszahlengenerator"
    assert "Minimum Number" in tool.input_params
    assert "Maximum Number" in tool.input_params
    assert "Amount of Rolls" in tool.input_params

def test_basic_generation():
    """Test basic random number generation"""
    tool = RandomNumberGeneratorTool()
    result = tool.execute_tool({
        "Minimum Number": "1",
        "Maximum Number": "10",
        "Amount of Rolls": "1"
    })
    
    assert result is True
    assert tool.output is not None
    assert len(tool.output.split(", ")) == 1
    assert 1 <= int(tool.output) <= 10

def test_multiple_rolls():
    """Test generating multiple random numbers"""
    tool = RandomNumberGeneratorTool()
    result = tool.execute_tool({
        "Minimum Number": "1",
        "Maximum Number": "100",
        "Amount of Rolls": "5"
    })
    
    assert result is True
    numbers = tool.output.split(", ")
    assert len(numbers) == 5
    for num in numbers:
        assert 1 <= int(num) <= 100

def test_negative_numbers():
    """Test generating random numbers with negative minimum"""
    tool = RandomNumberGeneratorTool()
    result = tool.execute_tool({
        "Minimum Number": "-10",
        "Maximum Number": "10",
        "Amount of Rolls": "3"
    })
    
    assert result is True
    numbers = tool.output.split(", ")
    assert len(numbers) == 3
    for num in numbers:
        assert -10 <= int(num) <= 10

def test_min_greater_than_max():
    """Test error handling when minimum is greater than maximum"""
    tool = RandomNumberGeneratorTool()
    result = tool.execute_tool({
        "Minimum Number": "20",
        "Maximum Number": "10",
        "Amount of Rolls": "1"
    })
    
    assert result is False
    assert "Das Minimum darf nicht größer als das Maximum sein" in tool.error_message

def test_empty_inputs():
    """Test error handling for empty inputs"""
    tool = RandomNumberGeneratorTool()
    result = tool.execute_tool({
        "Minimum Number": "",
        "Maximum Number": "10",
        "Amount of Rolls": "1"
    })
    
    assert result is False
    assert "Alle Eingabefelder müssen ausgefüllt sein." in tool.error_message

def test_non_numeric_inputs():
    """Test error handling for non-numeric inputs"""
    tool = RandomNumberGeneratorTool()
    result = tool.execute_tool({
        "Minimum Number": "abc",
        "Maximum Number": "10",
        "Amount of Rolls": "1"
    })
    
    assert result is False
    assert tool.error_message is not ""

def test_too_many_rolls():
    """Test error handling for too many rolls"""
    tool = RandomNumberGeneratorTool()
    result = tool.execute_tool({
        "Minimum Number": "1",
        "Maximum Number": "10",
        "Amount of Rolls": "1001"
    })
    
    assert result is False
    assert "Anzahl Würfe zu hoch" in tool.error_message

def test_large_numbers():
    """Test error handling for extremely large numbers"""
    tool = RandomNumberGeneratorTool()
    result = tool.execute_tool({
        "Minimum Number": str(sys.maxsize + 1),
        "Maximum Number": "10",
        "Amount of Rolls": "1"
    })
    
    assert result is False
    assert tool.error_message is not ""

def test_zero_rolls():
    """Test behavior with zero rolls"""
    tool = RandomNumberGeneratorTool()
    result = tool.execute_tool({
        "Minimum Number": "1",
        "Maximum Number": "10",
        "Amount of Rolls": "0"
    })
    
    assert result is False
    assert tool.error_message is not ""