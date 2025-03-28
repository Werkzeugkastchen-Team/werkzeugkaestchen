import pytest
from tools.placeholder_text.placeholder_text_tool import PlaceholderTextTool

class TestPlaceholderTextTool:
    def test_valid_length(self):
        tool = PlaceholderTextTool()
        input_params = {"length": "50"}
        
        result = tool.execute_tool(input_params)
        
        assert result is True
        assert tool.output is not None
        assert len(tool.output) > 0

    def test_too_large_length(self):
        tool = PlaceholderTextTool()
        input_params = {"length": "1001"}
        
        result = tool.execute_tool(input_params)
        
        assert result is False
        assert "Bitte geben Sie eine Zahl zwischen 1 und 1000 ein" in tool.error_message

    def test_invalid_length(self):
        tool = PlaceholderTextTool()
        input_params = {"length": "abc"}
        
        result = tool.execute_tool(input_params)
        
        assert result is False
        assert "Bitte geben Sie eine gültige Zahl ein" in tool.error_message

    def test_negative_length(self):
        tool = PlaceholderTextTool()
        input_params = {"length": "-10"}
        
        result = tool.execute_tool(input_params)
        
        assert result is False
        assert "Bitte geben Sie eine Zahl zwischen 1 und 1000 ein" in tool.error_message

    def test_zero_length(self):
        tool = PlaceholderTextTool()
        input_params = {"length": "0"}
        
        result = tool.execute_tool(input_params)
        
        assert result is False
        assert "Bitte geben Sie eine Zahl zwischen 1 und 1000 ein" in tool.error_message

    def test_missing_length(self):
        tool = PlaceholderTextTool()
        input_params = {}
        
        result = tool.execute_tool(input_params)
        
        assert result is False
        assert "Bitte geben Sie eine gültige Zahl ein" in tool.error_message

    def test_description_exists(self):
        tool = PlaceholderTextTool()
        assert tool.description is not None
        assert len(tool.description) > 0

    def test_name_correct(self):
        tool = PlaceholderTextTool()
        assert tool.name == "Platzhalter-Text Generator"

    def test_first_word_capitalized(self):
        tool = PlaceholderTextTool()
        input_params = {"length": "1"}
        
        result = tool.execute_tool(input_params)
        
        assert result is True
        text = tool.output.split('generatedText">')[1].split('</p>')[0].strip()
        assert text[0].isupper()

    def test_html_structure(self):
        tool = PlaceholderTextTool()
        input_params = {"length": "10"}
        
        result = tool.execute_tool(input_params)
        
        assert result is True
        assert '<div class="generated-text-container">' in tool.output
        assert '<p id="generatedText">' in tool.output
        assert '<button' in tool.output
        assert 'Kopieren' in tool.output 