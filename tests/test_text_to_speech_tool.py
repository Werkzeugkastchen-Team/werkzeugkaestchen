import unittest
import os
import tempfile
import uuid
from tools.text_to_speech.text_to_speech_tool import TextToSpeechTool
from tool_interface import OutputType

class TestTextToSpeechTool(unittest.TestCase):
    def setUp(self):
        self.tool = TextToSpeechTool()

    def test_execute_tool_success(self):
        input_params = {"text": "This is a test.", "voice": "en", "speed": "150", "pitch": "60", "volume": "120"}
        result = self.tool.execute_tool(input_params)
        self.assertTrue(result)
        self.assertIsInstance(self.tool.output, str)
        self.assertIn("Audio-Player:", self.tool.output)
        self.assertIsNone(self.tool.error_message)
        self.assertEqual(self.tool.output_type, OutputType.TEXT)

    def test_execute_tool_no_text(self):
        input_params = {"text": "", "voice": "en", "speed": "150", "pitch": "60", "volume": "120"}
        result = self.tool.execute_tool(input_params)
        self.assertFalse(result)
        self.assertIsNone(self.tool.output)
        self.assertIsNotNone(self.tool.error_message)
        self.assertEqual(self.tool.error_message, "Bitte geben Sie einen Text ein")

    def test_wav_file_deleted_after_base64(self):
        input_params = {"text": "This is a test.", "voice": "en", "speed": "150", "pitch": "60", "volume": "120"}
        self.tool.execute_tool(input_params)
        self.assertFalse(os.path.exists(self.tool.audio_file_path))

if __name__ == '__main__':
    unittest.main()
