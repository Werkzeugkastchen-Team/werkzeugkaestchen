# Python
import uuid
import tempfile
import os
import base64
from tool_interface import MiniTool, OutputType
from flask_babel import lazy_gettext as _

class TextToSpeechTool(MiniTool):
    name = _("Text zu Sprache")
    description = _("Konvertiert Text in gesprochene Sprache (TTS Text To Speech)")
    TTS_TOOL_CHARACTER_LIMIT = 6000

    def _get_audio_base64(self, audio_path):
        """Convert audio to base64 string for embedding in HTML"""
        with open(audio_path, "rb") as audio_file:
            return base64.b64encode(audio_file.read()).decode("utf-8")

    def __init__(self):
        super().__init__(self.name, "TextToSpeechTool")
        self.input_params = {_("Text"): "string", _("Sprache"): "string"}

    def execute_tool(self, input_params: dict) -> bool:
        try:
            self.error_message = None
            from TTS.api import TTS
            if not input_params.get(_("Text")) or not input_params.get(_("Sprache")):
                self.error_message = _("Alle Eingabefelder müssen ausgefüllt sein.")
                return False

            text = input_params.get(_("Text"), "")
            language = input_params.get(_("Sprache"), "de")

            if len(text) > self.TTS_TOOL_CHARACTER_LIMIT:
                self.error_message = _("Eingabetext darf wegen technischen Limitationen nicht länger als {0} Zeichen sein.").format(self.TTS_TOOL_CHARACTER_LIMIT)
                return False

            temp_dir = tempfile.gettempdir()
            uid = str(uuid.uuid4())
            filename = "output_" + uid + ".wav"
            filepath = os.path.join(temp_dir, filename)

            if text == "":
                self.error_message = _("Alle Eingabefelder müssen ausgefüllt sein.")
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

            # Textvariablen zur Übersetzung extern definieren
            header_audio = _("Sprachausgabe")
            unsupported = _("Your browser does not support the audio element.")
            download_audio = _("Audio herunterladen")
            header_details = _("Details")
            label_text = _("Text:")
            label_language = _("Sprache:")

            result = (
                f"<div class=\"text-to-speech-result\">"
                f"<div class=\"row\">"
                f"<div class=\"col-md-6\">"
                f"<div class=\"card\">"
                f"<div class=\"card-header bg-primary text-white\">"
                f"<h5 class=\"mb-0\">{header_audio}</h5>"
                f"</div>"
                f"<div class=\"card-body text-center\">"
                f"<audio controls>"
                f"<source src=\"data:audio/wav;base64,{audio_base64}\" type=\"audio/wav\">"
                f"{unsupported}"
                f"</audio>"
                f"<div class=\"mt-3\">"
                f"<a href=\"data:audio/wav;base64,{audio_base64}\" download=\"speech.wav\" class=\"fancy-button\">{download_audio}</a>"
                f"</div>"
                f"</div>"
                f"</div>"
                f"</div>"
                f"<div class=\"col-md-6\">"
                f"<div class=\"card\">"
                f"<div class=\"card-header bg-info text-white\">"
                f"<h5 class=\"mb-0\">{header_details}</h5>"
                f"</div>"
                f"<div class=\"card-body\">"
                f"<table class=\"table\">"
                f"<tbody>"
                f"<tr><th>{label_text}</th><td>{text}</td></tr>"
                f"<tr><th>{label_language}</th><td>{language}</td></tr>"
                f"</tbody>"
                f"</table>"
                f"</div>"
                f"</div>"
                f"</div>"
                f"</div>"
                f"</div>"
            )

            self.output = result
            self.error_message = None
            return True
        except Exception as e:
            self.error_message = str(e)
            return False