import pytest
from tools.word_counter.word_counter_tool import WordCounterTool

def test_word_counter_basic():
    tool = WordCounterTool()
    result = tool.execute_tool({"text": "Dies ist ein Test", "count_hyphens_as_one": False})
    assert result == True
    assert "4" in tool.output

def test_word_counter_empty():
    tool = WordCounterTool()
    result = tool.execute_tool({"text": "", "count_hyphens_as_one": False})
    assert result == False
    assert "Bitte geben Sie einen Text ein" in tool.error_message

def test_word_counter_with_hyphens_as_one():
    tool = WordCounterTool()
    test_cases = [
        ("E-Mail", 1),
        ("Server-Konfiguration", 1),
        ("Deutsch-Englisch-Wörterbuch", 1),
        ("E-Mail-Server-Konfiguration", 1)
    ]
    
    for text, expected_count in test_cases:
        result = tool.execute_tool({"text": text, "count_hyphens_as_one": True})
        assert result == True
        assert str(expected_count) in tool.output, f"Failed for input: {text}"

def test_word_counter_with_hyphens_as_separate():
    tool = WordCounterTool()
    test_cases = [
        ("E-Mail", 2),
        ("Server-Konfiguration", 2),
        ("Deutsch-Englisch-Wörterbuch", 3),
        ("E-Mail-Server-Konfiguration", 4)
    ]
    
    for text, expected_count in test_cases:
        result = tool.execute_tool({"text": text, "count_hyphens_as_one": False})
        assert result == True
        assert str(expected_count) in tool.output, f"Failed for input: {text}"

def test_word_counter_mixed_hyphen_cases():
    tool = WordCounterTool()
    text = "Die E-Mail-Adresse und der Web-Server sind offline"
    
    # Test with hyphens as one word
    result = tool.execute_tool({"text": text, "count_hyphens_as_one": True})
    assert result == True
    assert "5" in tool.output  # "Die", "E-Mail-Adresse", "und", "der", "Web-Server", "sind", "offline"
    
    # Test with hyphens as separate words
    result = tool.execute_tool({"text": text, "count_hyphens_as_one": False})
    assert result == True
    assert "9" in tool.output  # "Die", "E", "Mail", "Adresse", "und", "der", "Web", "Server", "sind", "offline"

def test_word_counter_with_multiple_hyphens_and_spaces():
    tool = WordCounterTool()
    text = "Der IT-Service-Desk    und     Help-Desk   sind   erreichbar"
    
    # Test with hyphens as one word
    result = tool.execute_tool({"text": text, "count_hyphens_as_one": True})
    assert result == True
    assert "5" in tool.output  # "Der", "IT-Service-Desk", "und", "Help-Desk", "sind", "erreichbar"
    
    # Test with hyphens as separate words
    result = tool.execute_tool({"text": text, "count_hyphens_as_one": False})
    assert result == True
    assert "9" in tool.output  # "Der", "IT", "Service", "Desk", "und", "Help", "Desk", "sind", "erreichbar"

def test_word_counter_with_multiple_spaces():
    tool = WordCounterTool()
    result = tool.execute_tool({"text": "Dies    ist   ein    Test", "count_hyphens_as_one": False})
    assert result == True
    assert "4" in tool.output

def test_word_counter_with_newlines():
    tool = WordCounterTool()
    result = tool.execute_tool({"text": "Dies\nist\nein\nTest", "count_hyphens_as_one": False})
    assert result == True
    assert "4" in tool.output 