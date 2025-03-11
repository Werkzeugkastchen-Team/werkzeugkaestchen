import pytest
from tools.word_counter.word_counter_tool import WordCounterTool

def test_word_counter_initialization():
    """Test if the tool initializes correctly"""
    tool = WordCounterTool()
    assert tool.name == "Wortzähler"
    assert "text" in tool.input_params
    assert "count_hyphens" in tool.input_params

def test_basic_word_count():
    """Test basic word counting functionality"""
    tool = WordCounterTool()
    result = tool.execute_tool({"text": "Dies ist ein Test", "count_hyphens": False})
    assert result == True
    assert "4" in tool.output  # Should count 4 words

def test_hyphenated_words_counted_as_one():
    """Test counting hyphenated words as one word"""
    tool = WordCounterTool()
    result = tool.execute_tool({"text": "E-Mail Server-Software", "count_hyphens": True})
    assert result == True
    assert "2" in tool.output  # Should count as 2 words

def test_hyphenated_words_counted_separately():
    """Test counting hyphenated parts as separate words"""
    tool = WordCounterTool()
    result = tool.execute_tool({"text": "E-Mail Server-Software", "count_hyphens": False})
    assert result == True
    assert "4" in tool.output  # Should count as 4 words

def test_multiple_spaces_and_newlines():
    """Test handling of multiple spaces and newlines"""
    tool = WordCounterTool()
    result = tool.execute_tool({
        "text": "Dies  ist\n\nein    Test\nmit    Zeilenumbrüchen",
        "count_hyphens": False
    })
    assert result == True
    assert "6" in tool.output  # Should count 6 words

def test_empty_input():
    """Test handling of empty input"""
    tool = WordCounterTool()
    result = tool.execute_tool({"text": "", "count_hyphens": False})
    assert result == False
    assert "Bitte geben Sie einen Text ein" in tool.error_message

def test_only_spaces_and_newlines():
    """Test handling of input with only spaces and newlines"""
    tool = WordCounterTool()
    result = tool.execute_tool({"text": "   \n\n   \t   ", "count_hyphens": False})
    assert result == False
    assert "Bitte geben Sie einen Text ein" in tool.error_message

def test_complex_hyphenation():
    """Test complex hyphenation scenarios"""
    tool = WordCounterTool()
    text = "Software-Entwicklung und Client-Server-Architektur"
    
    # Test with hyphens counted as one word
    result = tool.execute_tool({"text": text, "count_hyphens": True})
    assert result == True
    assert "3" in tool.output  # Should count as 3 words
    
    # Test with hyphens counted as separators
    result = tool.execute_tool({"text": text, "count_hyphens": False})
    assert result == True
    assert "6" in tool.output  # Should count as 6 words 