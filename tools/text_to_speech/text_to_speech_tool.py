import os
import tempfile
import subprocess
import uuid
from tool_interface import MiniTool, OutputType


class TextToSpeechTool(MiniTool):
    def __init__(self):
        super().__init__("Text to Speech", "TextToSpeechTool", output_type=OutputType.TEXT)
        self.description = "Konvertiert Text in gesprochene Sprache mit espeak"
        self.input_params = {
            "text": "string",
            "voice": "string",
            "speed": "string",
            "pitch": "string",
            "volume": "string"
        }
        # Store the path to the generated audio file
        self.audio_file_path = None

    def execute_tool(self, input_params: dict) -> bool:
        try:
            # Get parameters
            text = input_params.get("text", "")
            if not text:
                self.error_message = "Bitte geben Sie einen Text ein"
                return False

            # Get optional parameters with defaults
            voice = input_params.get("voice", "de")  # Default to German voice
            speed = input_params.get("speed", "100")  # Words per minute
            pitch = input_params.get("pitch", "50")   # 0-99
            volume = input_params.get("volume", "100")  # 0-200

            # Validate optional parameters
            if not voice:
                voice = "de"
            if not speed:
                speed = "100"
            if not pitch:
                pitch = "50"
            if not volume:
                volume = "100"

            # Create a unique ID for the audio file
            unique_id = uuid.uuid4()

            # Create the audio output file in the OS temp directory
            audio_file = os.path.join(tempfile.gettempdir(), f"speech_output_{unique_id}.wav")
            self.audio_file_path = audio_file

            # Build the espeak command as a string to match the working command
            espeak_cmd = f'espeak -v {voice} -s {speed} -p {pitch} -a {volume} -w "{audio_file}" "{text}"'

            # Execute espeak command as a shell command
            process = subprocess.run(
                espeak_cmd,
                shell=True,
                capture_output=True,
                text=True,
                check=False
            )

            # Check if the command was successful
            if process.returncode != 0:
                self.error_message = f"Fehler bei der Sprachsynthese: {process.stderr}"
                return False

            # Check if the file was created
            if not os.path.exists(audio_file):
                self.error_message = "Konnte keine Audiodatei erstellen"
                return False

            # Create a base64 representation of the audio file for embedding
            audio_base64 = self._get_audio_base64(audio_file)

            # Create HTML output with audio player and download link
            result = f"""
            <div class="text-to-speech-result">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">Ihre Sprachausgabe</h5>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <h6>Eingegebener Text:</h6>
                            <p class="border p-2 rounded">{text}</p>
                        </div>
                        
                        <div class="mb-3">
                            <h6>Audio-Player:</h6>
                            <audio controls class="w-100">
                                <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
                                Ihr Browser unterstützt das Audio-Element nicht.
                            </audio>
                        </div>
                        
                        <div class="mb-3">
                            <h6>Einstellungen:</h6>
                            <table class="table table-sm">
                                <tbody>
                                    <tr>
                                        <th>Stimme:</th>
                                        <td>{voice}</td>
                                    </tr>
                                    <tr>
                                        <th>Geschwindigkeit:</th>
                                        <td>{speed} Wörter pro Minute</td>
                                    </tr>
                                    <tr>
                                        <th>Tonhöhe:</th>
                                        <td>{pitch}</td>
                                    </tr>
                                    <tr>
                                        <th>Lautstärke:</th>
                                        <td>{volume}%</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        
                        <div class="text-center">
                            <a href="data:audio/wav;base64,{audio_base64}" 
                               download="{os.path.basename(audio_file)}" class="fancy-button">
                               Audio herunterladen
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            """

            self.output = result
            return True

        except Exception as e:
            self.error_message = f"Fehler bei der Sprachsynthese: {str(e)}"
            return False

    def _get_audio_base64(self, audio_path):
        """Convert audio file to base64 string for embedding in HTML"""
        import base64
        with open(audio_path, "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")
        os.remove(audio_path)
        return audio_base64
