# Python
import os
import tempfile
import uuid
from datetime import datetime, timedelta
from pydub import AudioSegment
from tool_interface import MiniTool, OutputType
from flask_babel import lazy_gettext as _

class AudioConverterTool(MiniTool):
    def __init__(self):
        super().__init__(_("Audio Konverter"), "AudioConverterTool", OutputType.TEXT)
        self.description = _("Konvertiert Audiodateien in verschiedene Formate (MP3, WAV, AAC, FLAC).")
        self.input_params = {
            "audio_file": "file",
            "target_format": "string"
        }
        self.current_format = None

    SUPPORTED_FORMATS = {
        'MP3': 'mp3',
        'WAV': 'wav',
        'AAC': 'aac',
        'FLAC': 'flac'
    }

    FORMAT_DISPLAY = {
        'MP3': 'MP3',
        'WAV': 'WAV',
        'AAC': 'AAC',
        'FLAC': 'FLAC'
    }

    pending_conversions = {}
    temp_dir = tempfile.gettempdir()

    def get_available_formats(self):
        """Returns list of available formats excluding the current format"""
        if not self.current_format:
            return ['MP3', 'WAV', 'AAC', 'FLAC']
        formats = ['MP3', 'WAV', 'AAC', 'FLAC']
        current_display = self.FORMAT_DISPLAY.get(self.current_format, self.current_format)
        if current_display in formats:
            formats.remove(current_display)
        return formats

    def execute_tool(self, input_params: dict) -> bool:
        try:
            if "audio_file" not in input_params:
                self.error_message = _("Bitte wählen Sie eine Audiodatei aus.")
                return False

            audio_info = input_params["audio_file"]
            target_format = input_params.get("target_format")

            if not target_format:
                self.error_message = _("Bitte wählen Sie ein Zielformat aus.")
                return False

            file_ext = os.path.splitext(audio_info["filename"])[1].lower()
            if file_ext not in ['.mp3', '.wav', '.aac', '.flac']:
                self.error_message = _("Das Format {0} wird nicht unterstützt. Bitte wählen Sie eine MP3, WAV, AAC oder FLAC Datei.").format(file_ext)
                return False

            token = str(uuid.uuid4())
            self.pending_conversions[token] = {
                "file_path": audio_info["file_path"],
                "target_format": target_format.lower(),
                "filename": os.path.splitext(audio_info["filename"])[0] + "." + target_format.lower(),
                "timestamp": datetime.now(),
                "downloaded": False
            }

            # Textvariablen extern festlegen
            alert_heading = _("Konvertierung erfolgreich!")
            message = _("Ihre Audiodatei wurde erfolgreich konvertiert. Klicken Sie auf den Button unten, um sie herunterzuladen.")
            download_text = _("Konvertierte Audiodatei herunterladen")
            another_text = _("Andere Audiodatei konvertieren")

            self.output = (
                f"<div class=\"alert alert-success\">"
                f"<h4 class=\"alert-heading\">{alert_heading}</h4>"
                f"<p>{message}</p>"
                f"<hr>"
                f"<div class=\"d-flex justify-content-between\">"
                f"<a href=\"/download_audio/{token}\" class=\"btn btn-primary\" download>{download_text}</a>"
                f"<a href=\"/tool/AudioConverterTool\" class=\"btn btn-secondary\">{another_text}</a>"
                f"</div>"
                f"</div>"
            )
            return True

        except Exception as e:
            self.error_message = _("Fehler bei der Konvertierung: ") + str(e)
            return False

    def convert_and_save(self, token):
        """Convert the audio file and return the path to the temporary file."""
        if token not in self.pending_conversions:
            print(_("Error: Token {0} not found in pending conversions").format(token))
            return None

        conversion = self.pending_conversions[token]
        if conversion["downloaded"]:
            print(_("Error: File for token {0} was already downloaded").format(token))
            return None

        try:
            if not os.path.exists(conversion["file_path"]):
                print(_("Error: Source file not found: {0}").format(conversion['file_path']))
                return None

            if os.path.getsize(conversion["file_path"]) == 0:
                print(_("Error: Source file is empty: {0}").format(conversion['file_path']))
                return None

            print(_("Loading audio file: {0}").format(conversion['file_path']))
            audio = AudioSegment.from_file(conversion["file_path"])
            target_format = conversion["target_format"].lstrip('.')
            output_path = os.path.join(self.temp_dir, f"converted_{token}.{target_format}")
            print(_("Converting to: {0}").format(output_path))

            if target_format == "aac":
                audio.export(output_path, format="adts", parameters=["-c:a", "aac", "-b:a", "192k"])
            else:
                audio.export(output_path, format=target_format)

            if not os.path.exists(output_path):
                print(_("Error: Converted file was not created: {0}").format(output_path))
                return None

            file_size = os.path.getsize(output_path)
            if file_size == 0:
                print(_("Error: Converted file is empty: {0}").format(output_path))
                return None

            print(_("Success: Converted file created with size {0} bytes").format(file_size))
            return output_path

        except Exception as e:
            print(_("Error converting audio: {0}").format(str(e)))
            import traceback
            print(_("Traceback: {0}").format(traceback.format_exc()))
            return None

    def cleanup_old_files(self):
        """Remove old conversions and their files."""
        now = datetime.now()
        tokens_to_remove = []

        for token, conversion in self.pending_conversions.items():
            if (now - conversion["timestamp"] > timedelta(hours=1) or conversion["downloaded"]):
                try:
                    if os.path.exists(conversion["file_path"]):
                        os.remove(conversion["file_path"])

                    converted_path = os.path.join(self.temp_dir, f"converted_{token}.{conversion['target_format']}")
                    if os.path.exists(converted_path):
                        os.remove(converted_path)
                except Exception as e:
                    print(_("Error cleaning up files: {0}").format(str(e)))

                tokens_to_remove.append(token)

        for token in tokens_to_remove:
            self.pending_conversions.pop(token, None)