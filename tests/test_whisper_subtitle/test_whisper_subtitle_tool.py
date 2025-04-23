import os
import os
import unittest
# Removed tempfile import as it's not directly used in the test logic anymore

from tools.whisper_subtitle.whisper_subtitle_tool import WhisperSubtitleTool


class TestWhisperSubtitleTool(unittest.TestCase):
    def setUp(self):
        self.tool = WhisperSubtitleTool()
        # Use the provided test audio file
        self.test_audio_path = os.path.join(os.path.dirname(__file__), "test.wav")
        # Ensure the test file exists before running tests
        if not os.path.exists(self.test_audio_path):
            self.fail(f"Test audio file not found at: {self.test_audio_path}")


    def tearDown(self):
        # No explicit cleanup needed for the input file as it's static.
        # The tool handles its own temporary SRT file cleanup.
        pass

    def test_execute_tool_success(self):
        input_params = {
            "input_file": self.test_audio_path, # Use the correct path
            "language": "english",
            "model_size": "tiny", # Use a small model for faster testing
            "task": "transcribe",
            # "embed_subtitles": False, # Removed parameter
        }
        success = self.tool.execute_tool(input_params)
        # Check for specific HTML content if possible, otherwise check non-empty
        self.assertTrue(success, f"Tool execution failed with error: {self.tool.error_message}")
        self.assertNotEqual(self.tool.output, "")

    def test_execute_tool_no_input_file(self):
        input_params = {
            "input_file": None,
            "language": "english",
            "model_size": "tiny",
            "task": "transcribe",
            # "embed_subtitles": False, # Removed parameter
        }
        success = self.tool.execute_tool(input_params)
        self.assertFalse(success)
        self.assertEqual(self.tool.error_message, "No input file provided.")

    def test_execute_tool_invalid_language(self):
        input_params = {
            "input_file": self.test_audio_path, # Use the correct path
            "language": "invalid_language", # Whisper should handle this internally
            "model_size": "tiny",
            "task": "transcribe",
            # "embed_subtitles": False, # Removed parameter
        }
        success = self.tool.execute_tool(input_params)
        # The tool should catch the error from Whisper and return False
        self.assertFalse(success)
        self.assertTrue(self.tool.error_message) # Check that an error message was set

    # Removed test_execute_tool_embed_subtitles as the feature is gone

if __name__ == "__main__":
    unittest.main()
