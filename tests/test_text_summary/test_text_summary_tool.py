import pytest
from unittest.mock import patch, MagicMock
from tools.text_summary.text_summary_tool import TextSummaryTool
from pydantic import ConfigDict
# No need to import litellm.completion here anymore for mocking purposes

class TestTextSummaryTool:
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Patch 'completion' in the 'litellm' module where it's actually imported from
    @patch('litellm.completion')
    def test_basic_summary(self, mock_completion_func):
        """Test basic text summarization with mocked LLM response"""
        tool = TextSummaryTool()
        input_text = "This is a long text that needs to be summarized."
        expected_summary = "Short summary."
        input_params = {"Text": input_text}

        # Configure the mock object passed by @patch
        # Create a mock response structure that mimics litellm's response
        mock_message = MagicMock()
        mock_message.content = expected_summary
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        mock_completion_func.return_value = mock_response # Set the return value of the mocked function

        result = tool.execute_tool(input_params)

        # Assertions
        assert result is True
        assert tool.output == expected_summary
        assert tool.error_message == ""
        # Check if the mock was called correctly
        mock_completion_func.assert_called_once()
        call_args, call_kwargs = mock_completion_func.call_args
        assert call_kwargs.get("model") == "ollama/gemma3:1b"
        assert "messages" in call_kwargs
        assert len(call_kwargs["messages"]) == 1
        assert input_text in call_kwargs["messages"][0]["content"]


    def test_empty_input(self):
        """Test handling of empty input text"""
        tool = TextSummaryTool()
        input_params = {"Text": ""}

        result = tool.execute_tool(input_params)

        assert result is False
        assert tool.error_message == "Input text is empty or invalid"
        assert tool.output == ""

    def test_missing_input(self):
        """Test handling when 'Text' parameter is missing"""
        tool = TextSummaryTool()
        input_params = {} # Missing "Text" key

        result = tool.execute_tool(input_params)

        assert result is False
        assert tool.error_message == "Input text is empty or invalid"
        assert tool.output == ""

    # Patch 'completion' in the 'litellm' module where it's actually imported from
    @patch('litellm.completion')
    def test_llm_error(self, mock_completion_func):
        """Test handling when litellm completion raises an exception"""
        tool = TextSummaryTool()
        input_params = {"Text": "Some text"}
        error_message = "LLM API error"

        # Configure the mock to raise an exception when called
        mock_completion_func.side_effect = Exception(error_message)

        result = tool.execute_tool(input_params)

        assert result is False
        assert tool.error_message == error_message
        assert tool.output == ""
        mock_completion_func.assert_called_once() # Ensure it was still called
