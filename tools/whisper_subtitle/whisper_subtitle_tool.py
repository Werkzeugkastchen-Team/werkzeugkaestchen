import os
import subprocess
import tempfile
from enum import Enum

import torch
import whisper
from whisper.utils import get_writer

from tool_interface import MiniTool, OutputType
from tools.whisper_subtitle.languages import LANGUAGES

FULL_TO_CODE = {v: k for k, v in LANGUAGES.items()}

class Task(Enum):
    TRANSCRIBE = "transcribe"
    TRANSLATE = "translate"

class ModelSize(Enum):
    TINY = "tiny"
    BASE = "base"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    LARGETURBO = "large-v3-turbo"
    TURBO = "turbo"
    TINYEN = "tiny.en"
    BASEEN = "base.en"
    SMALLEN = "small.en"
    MEDIUMEN = "medium.en"

class WhisperSubtitleTool(MiniTool):
    def __init__(self):
        super().__init__(
            name="Whisper Subtitle",
            identifier="whisper_subtitle",
            output_type=OutputType.FILE,
        )
        self.description = "Generates subtitles for a video file using Whisper."
        self.input_params = {
            "input_file": {
                "type": "file",
                "description": "Path to the video file.",
                "required": True,
            },
            "language": {
                "type": "string",
                "description": "Language of the video.",
                "required": True,
                "options": list(LANGUAGES.values()),
                "default": LANGUAGES["en"],
            },
            "model_size": {
                "type": "string",
                "description": "Whisper model size.",
                "required": True,
                "options": [e.value for e in ModelSize],
                "default": ModelSize.TINY.value,
            },
            "task": {
                "type": "string",
                "description": "Task to perform (transcribe or translate).",
                "required": True,
                "options": [e.value for e in Task],
                "default": Task.TRANSCRIBE.value,
            },
            "embed_subtitles": {
                "type": "boolean",
                "description": "Embed subtitles into the video file (ffmpeg required).",
                "required": False,
                "default": False,
            },
        }

    def execute_tool(self, input_params: dict) -> bool:
        try:
            input_file = input_params.get("input_file")
            language = input_params.get("language")
            model_size = input_params.get("model_size")
            task = input_params.get("task")
            embed_subtitles = input_params.get("embed_subtitles", False)

            if not input_file:
                self.error_message = "No input file provided."
                return False

            # ytdlp_functions will give us a string, gradio filepicker an actual file
            input_file_cleared = input_file if isinstance(input_file, str) else input_file.name

            print("gpu available: " + str(torch.cuda.is_available()))
            gpu = torch.cuda.is_available()
            model = whisper.load_model(model_size)

            whisper_output = model.transcribe(
                input_file_cleared,
                task=task,
                language=FULL_TO_CODE[language],
                verbose=True,
                fp16=gpu,
            )

            temp_dir = str(tempfile.gettempdir())
            writer = get_writer("srt", temp_dir)
            writer(whisper_output, input_file_cleared)

            srt_file = os.path.join(
                temp_dir, os.path.basename(input_file_cleared).rsplit(".", 1)[0] + ".srt"
            )

            if embed_subtitles:
                video_out = input_file_cleared + "_output.mkv"
                try:
                    command = [
                        "ffmpeg",
                        "-i",
                        input_file_cleared,
                        "-vf",
                        f"subtitles={srt_file}",
                        "-c:a",
                        "copy",
                        video_out,
                    ]
                    subprocess.run(command, check=True, capture_output=True, text=True)
                except subprocess.CalledProcessError as e:
                    print(e.stderr)
                    self.error_message = "ffmpeg failed to embed subtitles into video"
                    return False
                self.output = video_out
            else:
                self.output = srt_file

            return True

        except Exception as e:
            self.error_message = str(e)
            return False


if __name__ == "__main__":
    # Example usage
    tool = WhisperSubtitleTool()
    input_params = {
        "input_file": "test.mp4",  # Replace with a valid video file
        "language": "english",
        "model_size": "tiny",
        "task": "transcribe",
        "embed_subtitles": False,
    }
    success = tool.execute_tool(input_params)

    if success:
        print("Subtitle generation successful!")
        print("Output file:", tool.output)
    else:
        print("Subtitle generation failed.")
        print("Error message:", tool.error_message)
