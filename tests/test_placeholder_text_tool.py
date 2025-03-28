import pytest
from tools.placeholder_text.placeholder_text_tool import PlaceholderTextTool

class TestPlaceholderTextTool:
    def test_valid_length(self):
        tool = PlaceholderTextTool()
        input_params = {"length": "50"}
        
        result = tool.execute_tool(input_params)
        
        assert result is True
        assert len(tool.output.split()) == 50
        
    def test_too_large_length(self):
        tool = PlaceholderTextTool()
        input_params = {"length": "1001"}
        
        result = tool.execute_tool(input_params)
        
        assert result is False
        assert "zwischen 1 und 1000" in tool.error_message
        
    def test_invalid_length(self):
        tool = PlaceholderTextTool()
        input_params = {"length": "abc"}
        
        result = tool.execute_tool(input_params)
        
        assert result is False
        assert "gültige Zahl" in tool.error_message
        
    def test_negative_length(self):
        tool = PlaceholderTextTool()
        input_params = {"length": "-10"}
        
        result = tool.execute_tool(input_params)
        
        assert result is False
        assert "zwischen 1 und 1000" in tool.error_message

    def test_first_letter_capitalized(self):
        tool = PlaceholderTextTool()
        input_params = {"length": "1"}
        
        result = tool.execute_tool(input_params)
        
        assert result is True
        assert tool.output[0].isupper() 