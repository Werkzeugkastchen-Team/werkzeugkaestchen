import pytest
from tools.json_validieren.json_validieren_tool import JSONValidierungTool

def test_json_tool_initialization():
    tool = JSONValidierungTool()
    assert tool.name == "JSON-Validierung"
    assert "JSON Text" in tool.input_params

def test_valid_json():
    tool = JSONValidierungTool()
    valid_json = '{"name": "Anna", "alter": 25}'
    result = tool.execute_tool({"JSON Text": valid_json})
    
    assert result is True
    assert tool.is_valid is True
    assert "alert-success" in tool.output

def test_invalid_json():
    tool = JSONValidierungTool()
    invalid_json = '{"name": "Anna", alter: 25}'  # Fehlende Anführungszeichen
    result = tool.execute_tool({"JSON Text": invalid_json})
    
    assert result is True
    assert tool.is_valid is False
    assert "Ungültiges JSON" in tool.output
    assert "Zeile" in tool.output  # Prüft Positionsangabe

def test_empty_input():
    tool = JSONValidierungTool()
    result = tool.execute_tool({"JSON Text": ""})
    
    assert result is False
    assert "Bitte geben Sie JSON-Text ein" in tool.error_message

def test_edge_cases():
    tool = JSONValidierungTool()
    # Test mit verschachteltem JSON
    nested_json = '{"data": {"users": [{"id": 1}, {"id": 2}]}}'
    assert tool.execute_tool({"JSON Text": nested_json}) is True