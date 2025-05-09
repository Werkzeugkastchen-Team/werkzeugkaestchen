import pytest
from tools.base64_decode.base64_decode_tool import Base64DecodeTool


class TestBase64DecodeTool:
    def test_basic_decoding(self):
        """Test basic base64 decoding"""
        tool = Base64DecodeTool()
        input_params = {"Zu dekodierender Base64-String": "SGVsbG8gV29ybGQ="}

        result = tool.execute_tool(input_params)

        assert result is True
        assert tool.output == "Hello World"
        assert tool.error_message == ""

    def test_ascii_decoding(self):
        """Test ascii base64 decoding"""
        tool = Base64DecodeTool()
        input_params = {
            "Zu dekodierender Base64-String": "SGVsbG8gV29ybGQ=",
            "Kodierung": "ascii",
        }

        result = tool.execute_tool(input_params)

        assert result is True
        assert tool.output == "Hello World"
        assert tool.error_message == ""

    def test_utf8_decoding(self):
        """Test utf-8 base64 decoding"""
        tool = Base64DecodeTool()
        input_params = {
            "Zu dekodierender Base64-String": "U8O8cGVy8J+ltA==",
            "Kodierung": "utf-8",
        }

        result = tool.execute_tool(input_params)

        assert result is True
        assert tool.output == "Süper🥴"
        assert tool.error_message == ""

    def test_decoding_mismatch(self):
        """Test decoding mismatch"""
        tool = Base64DecodeTool()
        input_params = {
            "Zu dekodierender Base64-String": "U8O8cGVy8J+ltA==",
            "Kodierung": "ascii",
        }

        result = tool.execute_tool(input_params)

        assert result is False
        assert tool.error_message is not ""

    def test_empty_input(self):
        """Test handling of empty input"""
        tool = Base64DecodeTool()
        input_params = {"Zu dekodierender Base64-String": ""}

        result = tool.execute_tool(input_params)

        assert result is False
        assert tool.error_message == "Base64-Eingabestring ist leer oder ungültig"

    def test_missing_input_params(self):
        """Test handling when required input is missing"""
        tool = Base64DecodeTool()
        input_params = {}

        result = tool.execute_tool(input_params)

        assert result is False
        assert tool.error_message == "Base64-Eingabestring ist leer oder ungültig"
