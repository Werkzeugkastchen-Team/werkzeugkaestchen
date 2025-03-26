from TTS.api import TTS
import uuid
import tempfile
import os
from tool_interface import MiniTool, OutputType
import base64

class TextToSpeechTool(MiniTool):
    name = "Text zu Sprache"
    description = "Konvertiert Text in gesprochene Sprache (TTS Text To Speech)"
    
    TTS_TOOL_CHARACTER_LIMIT = 600

    def _get_audio_base64(self, audio_path):
        """Convert audio to base64 string for embedding in HTML"""
        with open(audio_path, "rb") as audio_file:
            return base64.b64encode(audio_file.read()).decode("utf-8")

    def __init__(self):
        super().__init__(self.name, "TextToSpeechTool")
        self.input_params = {"Text": "string", "Sprache": "string"}

    def execute_tool(self, input_params:dict) -> bool:
        try:
            self.error_message = None
            if not input_params.get("Text") or not input_params.get("Sprache"):
                self.error_message = "Alle Eingabefelder müssen ausgefüllt sein."
                return False

            text = input_params.get("Text", "")
            language = input_params.get("Sprache", "de")
            
            if len(text) > self.TTS_TOOL_CHARACTER_LIMIT:
                self.error_message = f"Eingabetext darf wegen technischen Limitationen nicht länger als {self.TTS_TOOL_CHARACTER_LIMIT} Zeichen sein."
                return False
            
            temp_dir = tempfile.gettempdir()
            id = str(uuid.uuid4())
            filename = str("output_" + id + ".wav")
            filepath = os.path.join(temp_dir,filename)
            if text == "":
                self.error_message = "Alle Eingabefelder müssen ausgefüllt sein."
                return False

            tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

            tts.tts_to_file(
                text=text,
                file_path=filepath,
                speaker="Ana Florence",
                language=language,
                split_sentences=True,
            )

            audio_base64 = self._get_audio_base64(filepath)

            result = f"""
            <div class="text-to-speech-result">
                <div class="row">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header bg-primary text-white">
                                <h5 class="mb-0">Sprachausgabe</h5>
                            </div>
                            <div class="card-body text-center">
                                <audio controls>
                                    <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
                                    Your browser does not support the audio element.
                                </audio>
                                <div class="mt-3">
                                    <a href="data:audio/wav;base64,{audio_base64}" 
                                       download="speech.wav" class="fancy-button">
                                       Audio herunterladen
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
                                            <th>Text:</th>
                                            <td>{text}</td>
                                        </tr>
                                        <tr>
                                            <th>Sprache:</th>
                                            <td>{language}</td>
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
            self.error_message = None
            return True
        except Exception as e:
            self.error_message = str(e)
            return False
