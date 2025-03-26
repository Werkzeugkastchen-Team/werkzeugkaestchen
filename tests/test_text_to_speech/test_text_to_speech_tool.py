import pytest
from tools.text_to_speech.text_to_speech_tool import TextToSpeechTool
from unittest.mock import patch

@pytest.fixture
def tool():
    return TextToSpeechTool()

def test_initialization():
    tool = TextToSpeechTool()
    assert tool is not None

def test_successful_execution(tool):
    input_params = {"Text": "This is a test.", "Sprache": "de"}
    result = tool.execute_tool(input_params)
    assert result is True
    assert tool.error_message is None
    assert isinstance(tool.output, str)
    assert "<audio controls>" in tool.output

def test_error_handling_missing_input(tool):
    with patch("builtins.input", return_value="y"):
        input_params = {"Text": ""}
        result = tool.execute_tool(input_params)
        assert result is False
        assert tool.error_message is not None

def test_output_contains_base64_audio(tool):
    with patch("builtins.input", return_value="y"):
        input_params = {"Text": "This is a test.", "Sprache": "de"}
        tool.execute_tool(input_params)
        assert "base64," in tool.output
    # Further validation of the base64 string would require decoding and checking the audio data
