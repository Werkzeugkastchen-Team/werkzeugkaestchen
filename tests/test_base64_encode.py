import pytest
from tools.base64_encode.base64_encode_tool import Base64EncodeTool

class TestBase64EncodeTool:
    def test_basic_encoding(self):
        """Test basic text encoding with default utf-8 encoding"""
        tool = Base64EncodeTool()
        input_params = {"Zu kodierender Text": "Hello World"}
        
        result = tool.execute_tool(input_params)
        
        assert result is True
        assert tool.output == "SGVsbG8gV29ybGQ="
        assert tool.error_message == ""
    
    def test_empty_input(self):
        """Test handling of empty input"""
        tool = Base64EncodeTool()
        input_params = {"Zu kodierender Text": ""}
        
        result = tool.execute_tool(input_params)
        
        assert result is False
        assert tool.error_message == "Eingabetext ist leer oder ungültig"
    
    def test_ascii_encoding(self):
        """Test encoding with ASCII encoding option"""
        tool = Base64EncodeTool()
        input_params = {"Zu kodierender Text": "Hello World", "Kodierung": "ascii"}
        
        result = tool.execute_tool(input_params)
        
        assert result is True
        assert tool.output == "SGVsbG8gV29ybGQ="
        assert tool.error_message == ""
    
    def test_special_characters(self):
        """Test encoding of text with special characters"""
        tool = Base64EncodeTool()
        input_params = {"Zu kodierender Text": "Héllö Wörld!"}
        
        result = tool.execute_tool(input_params)
        
        assert result is True
        assert tool.output == "SMOpbGzDtiBXw7ZybGQh"
        assert tool.error_message == ""
    
    def test_missing_input(self):
        """Test handling when required input is missing"""
        tool = Base64EncodeTool()
        input_params = {}
        
        result = tool.execute_tool(input_params)

        assert result is False
        assert tool.error_message == "Eingabetext ist leer oder ungültig"