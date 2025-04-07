import os
import tempfile
import unittest

from tools.whisper_subtitle.whisper_subtitle_tool import WhisperSubtitleTool


class TestWhisperSubtitleTool(unittest.TestCase):
    def setUp(self):
        self.tool = WhisperSubtitleTool()
        self.test_video = "test.mp4"  # Replace with a valid video file for testing
        # Create a dummy video file for testing
        with open(self.test_video, "w") as f:
            f.write("Dummy video content")

    def tearDown(self):
        # Clean up the dummy video file
        if os.path.exists(self.test_video):
            os.remove(self.test_video)
        # Clean up the srt file
        srt_file = self.test_video.rsplit(".", 1)[0] + ".srt"
        if os.path.exists(srt_file):
            os.remove(srt_file)
        # Clean up the video_out file
        video_out = self.test_video + "_output.mkv"
        if os.path.exists(video_out):
            os.remove(video_out)

    def test_execute_tool_success(self):
        input_params = {
            "input_file": self.test_video,
            "language": "english",
            "model_size": "tiny",
            "task": "transcribe",
            "embed_subtitles": False,
        }
        success = self.tool.execute_tool(input_params)
        self.assertTrue(success)
        self.assertNotEqual(self.tool.output, "")

    def test_execute_tool_no_input_file(self):
        input_params = {
            "input_file": None,
            "language": "english",
            "model_size": "tiny",
            "task": "transcribe",
            "embed_subtitles": False,
        }
        success = self.tool.execute_tool(input_params)
        self.assertFalse(success)
        self.assertEqual(self.tool.error_message, "No input file provided.")

    def test_execute_tool_invalid_language(self):
        input_params = {
            "input_file": self.test_video,
            "language": "invalid_language",
            "model_size": "tiny",
            "task": "transcribe",
            "embed_subtitles": False,
        }
        success = self.tool.execute_tool(input_params)
        # The whisper library will throw an error if the language is invalid
        self.assertFalse(success)

    def test_execute_tool_embed_subtitles(self):
        input_params = {
            "input_file": self.test_video,
            "language": "english",
            "model_size": "tiny",
            "task": "transcribe",
            "embed_subtitles": True,
        }
        success = self.tool.execute_tool(input_params)
        # The test will fail if ffmpeg is not installed
        self.assertTrue(success)
        self.assertNotEqual(self.tool.output, "")


if __name__ == "__main__":
    unittest.main()
