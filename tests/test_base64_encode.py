import pytest
from tools.base64_encode.base64_encode_tool import Base64EncodeTool

class TestBase64EncodeTool:
    def test_basic_encoding(self):
        """Test basic text encoding with default utf-8 encoding"""
        # Arrange
        tool = Base64EncodeTool()
        input_params = {"Text to encode": "Hello World"}
        
        # Act
        result = tool.execute_tool(input_params)
        
        # Assert
        assert result is True
        assert tool.output == "SGVsbG8gV29ybGQ="
        assert tool.error_message == ""
    
    def test_empty_input(self):
        """Test handling of empty input"""
        # Arrange
        tool = Base64EncodeTool()
        input_params = {"Text to encode": ""}
        
        # Act
        result = tool.execute_tool(input_params)
        
        # Assert
        assert result is False
        assert tool.error_message == "Input text is empty or invalid"
    
    def test_ascii_encoding(self):
        """Test encoding with ASCII encoding option"""
        # Arrange
        tool = Base64EncodeTool()
        input_params = {"Text to encode": "Hello World", "Encoding": "ascii"}
        
        # Act
        result = tool.execute_tool(input_params)
        
        # Assert
        assert result is True
        assert tool.output == "SGVsbG8gV29ybGQ="
        assert tool.error_message == ""
    
    def test_special_characters(self):
        """Test encoding of text with special characters"""
        # Arrange
        tool = Base64EncodeTool()
        input_params = {"Text to encode": "Héllö Wörld!"}
        
        # Act
        result = tool.execute_tool(input_params)
        
        # Assert
        assert result is True
        assert tool.output == "SMOpbGzDtiBXw7ZybGQh"
        assert tool.error_message == ""
    
    def test_missing_input(self):
        """Test handling when required input is missing"""
        # Arrange
        tool = Base64EncodeTool()
        input_params = {}
        
        # Act
        result = tool.execute_tool(input_params)
        
        # Assert
        assert result is False
        assert tool.error_message == "Input text is empty or invalid"