import os
import subprocess
import tempfile
from enum import Enum

import torch
import base64 # Added import

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
            identifier="WhisperSubtitleTool"
        )
        self.description = "Generates subtitles (SRT) for an audio/video file using Whisper." # Updated description
        self.input_params = {
            "input_file": "file",
            "language": "string",
            "model_size": "string",
            "task": "string",
            # Removed "embed_subtitles"
        }

    def execute_tool(self, input_params: dict) -> bool:
        try:
            input_file = input_params.get("input_file")
            language = input_params.get("language")
            model_size = input_params.get("model_size")
            task = input_params.get("task")
            # Removed embed_subtitles

            if not input_file:
                self.error_message = "No input file provided."
                return False

            # Handle different input types: string path, dictionary (from Flask), or object with 'name'
            if isinstance(input_file, str):
                input_file_cleared = input_file
            elif isinstance(input_file, dict):
                input_file_cleared = input_file.get('file_path') # Use 'file_path' key
                input_filename = input_file.get('filename', os.path.basename(input_file_cleared) if input_file_cleared else 'unknown_file') # Get original filename if possible
            else:
                input_file_cleared = getattr(input_file, 'name', None)
                input_filename = os.path.basename(input_file_cleared) if input_file_cleared else 'unknown_file' # Get original filename if possible

            # Validate that we obtained a valid path string
            if not input_file_cleared or not isinstance(input_file_cleared, str):
                self.error_message = "Could not determine input file path from provided input."
                return False

            # Validate input file existence
            if not os.path.exists(input_file_cleared):
                self.error_message = f"Input file '{input_file_cleared}' does not exist."
                return False

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
            audio = whisper.load_audio(input_file_cleared)
            if audio is None or len(audio) == 0:
                self.error_message = f"Failed to load audio data from '{input_file_cleared}'"
                return False

            writer = get_writer("srt", temp_dir)
            # Pass the input file path, not the loaded audio array
            writer(whisper_output, input_file_cleared)

            srt_file = os.path.join(
                temp_dir, os.path.basename(input_filename).rsplit(".", 1)[0] + ".srt" # Use original filename for SRT name
            )

            # Read SRT content and encode as Base64
            try:
                with open(srt_file, "r", encoding="utf-8") as f:
                    srt_content = f.read()
                srt_base64 = base64.b64encode(srt_content.encode("utf-8")).decode("utf-8")
                # Clean up temporary SRT file after reading
                os.remove(srt_file)
            except Exception as e:
                self.error_message = f"Failed to read or encode SRT file: {e}"
                return False

            # Construct HTML output
            download_filename = os.path.basename(srt_file)
            result = f"""
            <div class="whisper-subtitle-result">
                <div class="row">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header bg-primary text-white">
                                <h5 class="mb-0">Subtitle File</h5>
                            </div>
                            <div class="card-body text-center">
                                <p>Subtitles generated successfully.</p>
                                <div class="mt-3">
                                    <a href="data:text/plain;charset=utf-8;base64,{srt_base64}"
                                       download="{download_filename}" class="fancy-button">
                                       Download SRT File
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header bg-info text-white">
                                <h5 class="mb-0">Details</h5>
                            </div>
                            <div class="card-body">
                                <table class="table">
                                    <tbody>
                                        <tr>
                                            <th>Input File:</th>
                                            <td>{input_filename}</td>
                                        </tr>
                                        <tr>
                                            <th>Language:</th>
                                            <td>{language}</td>
                                        </tr>
                                        <tr>
                                            <th>Model Size:</th>
                                            <td>{model_size}</td>
                                        </tr>
                                        <tr>
                                            <th>Task:</th>
                                            <td>{task}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """
            self.output = result
            return True

        except Exception as e:
            self.error_message = str(e)
            return False


if __name__ == "__main__":
    # Example usage
    tool = WhisperSubtitleTool()
    # Example usage (Note: Output is now HTML, not a file path)
    tool = WhisperSubtitleTool()
    # Create a dummy input file for testing if needed
    dummy_file_path = "dummy_audio.mp3"
    if not os.path.exists(dummy_file_path):
         with open(dummy_file_path, "w") as f:
             f.write("dummy content") # Whisper might fail, but tests path handling

    input_params = {
        "input_file": dummy_file_path, # Use dummy file or replace with a real one
        "language": "english",
        "model_size": "tiny",
        "task": "transcribe",
        # embed_subtitles removed
    }
    # Example with dictionary input
    # input_params = {
    #     "input_file": {'file_path': dummy_file_path, 'filename': 'dummy_audio.mp3'},
    #     "language": "english",
    #     "model_size": "tiny",
    #     "task": "transcribe",
    # }

    success = tool.execute_tool(input_params)

    if success:
        print("Subtitle generation successful! Output is HTML:")
        # print(tool.output) # Uncomment to see HTML
    else:
        print("Subtitle generation failed.")
        print("Error message:", tool.error_message)
