import pytest
from tools.json_formatieren.json_formatieren_tool import JSONFormatierungTool

def test_valid_json_formatting():
    tool = JSONFormatierungTool()
    valid_json = '{"name":"Anna","age":25}'
    result = tool.execute_tool({"JSON Text": valid_json})
    
    assert result is True
    assert "    \"name\": \"Anna\"," in tool.output

def test_invalid_json():
    tool = JSONFormatierungTool()
    result = tool.execute_tool({"JSON Text": "{invalid}"})
    
    assert result is True
    assert "ungültiges json" in tool.output.lower()

def test_copy_button_existence():
    tool = JSONFormatierungTool()
    tool.execute_tool({"JSON Text": '{"test": true}'})
    
    assert "copyToClipboard()" in tool.output
    assert "btn btn-success" in tool.output