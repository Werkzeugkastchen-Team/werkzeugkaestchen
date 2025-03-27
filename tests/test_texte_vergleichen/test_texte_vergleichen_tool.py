import pytest
from tools.texte_vergleichen.texte_vergleichen_tool import TexteVergleichenTool

def test_texte_vergleichen_tool_initialization():
    """Test the initialization of the TexteVergleichenTool"""
    tool = TexteVergleichenTool()
    assert tool.name == "Textvergleich"
    # Changed from tool_id to check the second parameter passed to super().__init__()
    assert hasattr(tool, 'input_params')
    assert "text1" in tool.input_params
    assert "text2" in tool.input_params

def test_texte_vergleichen_empty_input():
    """Test the tool's behavior with empty input"""
    tool = TexteVergleichenTool()
    result = tool.execute_tool({"text1": "", "text2": ""})
    
    assert result is False
    assert "Bitte geben Sie beide Texte zum Vergleich ein." in tool.error_message

def test_texte_vergleichen_identical_texts():
    """Test comparison of identical texts"""
    tool = TexteVergleichenTool()
    text = "Dies ist ein Testtext für den Vergleich."
    
    result = tool.execute_tool({"text1": text, "text2": text})
    
    assert result is True
    assert tool.similarity_score == 100.0
    assert "Ähnlichkeit: 100.0%" in tool.output

def test_texte_vergleichen_different_texts():
    """Test comparison of different texts"""
    tool = TexteVergleichenTool()
    text1 = "Der schnelle braune Fuchs springt über den Zaun."
    text2 = "Der langsame graue Hund läuft neben dem Zaun."
    
    result = tool.execute_tool({"text1": text1, "text2": text2})
    
    assert result is True
    assert 0 < tool.similarity_score < 100.0
    assert "Ähnlichkeit:" in tool.output

def test_texte_vergleichen_html_output():
    """Test the HTML output of the tool"""
    tool = TexteVergleichenTool()
    # Changed texts to ensure we get all comparison types
    text1 = "Python ist eine großartige Programmiersprache für Anfänger."
    text2 = "Python ist eine tolle Skriptsprache für Experten."
    
    result = tool.execute_tool({"text1": text1, "text2": text2})
    
    assert result is True
    html_output = tool.output
    
    # Check for key HTML elements and classes
    assert "<html>" in html_output
    assert "text-comparison-result" in html_output
    assert "class=\"similar\"" in html_output  # For matching words
    assert "class=\"replaced\"" in html_output  # For replaced words
    # Check that at least one difference type is present
    assert any(
        cls in html_output 
        for cls in ['class="deleted"', 'class="added"', 'class="replaced"']
    )

def test_texte_vergleichen_edge_cases():
    """Test various edge cases"""
    tool = TexteVergleichenTool()
    
    # Test with whitespace-only texts
    result_whitespace = tool.execute_tool({"text1": "   ", "text2": "   "})
    assert result_whitespace is False
    
    # Test with very long texts
    long_text1 = "Python " * 1000
    long_text2 = "Python " * 1000 + "Programmieren"
    
    result_long = tool.execute_tool({"text1": long_text1, "text2": long_text2})
    assert result_long is True
    assert tool.similarity_score > 99.0

def test_texte_vergleichen_special_characters():
    """Test handling of special characters and Unicode"""
    tool = TexteVergleichenTool()
    text1 = "Hallo, wie geht's? Das ist ein Test! #Python"
    text2 = "Hallo, wie geht es? Das ist ein Test #Python!"
    
    result = tool.execute_tool({"text1": text1, "text2": text2})
    
    assert result is True
    assert 0 < tool.similarity_score < 100.0

def test_texte_vergleichen_error_handling():
    """Test error handling mechanism"""
    tool = TexteVergleichenTool()
    
    # Changed to test the actual error handling behavior
    result = tool.execute_tool({"text1": None, "text2": None})
    assert result is False
    assert "Fehler beim Textvergleich" in tool.error_message