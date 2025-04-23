import os
import tempfile
import uuid
import time
from pydub import AudioSegment
from tool_interface import MiniTool, OutputType
from datetime import datetime, timedelta

class AudioConverterTool(MiniTool):
    name = "Audio Konverter"
    description = "Konvertiert Audiodateien in verschiedene Formate (MP3, WAV, AAC, FLAC)."
    
    SUPPORTED_FORMATS = {
        'MP3': 'mp3',
        'WAV': 'wav',
        'AAC': 'aac',
        'FLAC': 'flac'
    }
    
    # Add format display names mapping
    FORMAT_DISPLAY = {
        'MP3': 'MP3',
        'WAV': 'WAV',
        'AAC': 'AAC',
        'FLAC': 'FLAC'
    }
    
    # Class variable to store pending conversions
    pending_conversions = {}
    temp_dir = tempfile.gettempdir()  # Get system's temp directory
    
    def __init__(self):
        super().__init__(self.name, "AudioConverterTool", OutputType.TEXT)
        self.input_params = {
            "audio_file": "file",
            "target_format": "string"
        }
        self.current_format = None
    
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
                self.error_message = "Bitte wählen Sie eine Audiodatei aus."
                return False
            
            audio_info = input_params["audio_file"]
            target_format = input_params.get("target_format")
            
            if not target_format:
                self.error_message = "Bitte wählen Sie ein Zielformat aus."
                return False
            
            # Validate file type
            file_ext = os.path.splitext(audio_info["filename"])[1].lower()
            if file_ext not in ['.mp3', '.wav', '.aac', '.flac']:
                self.error_message = f"Das Format {file_ext} wird nicht unterstützt. Bitte wählen Sie eine MP3, WAV, AAC oder FLAC Datei."
                return False
            
            # Generate a unique token for this conversion
            token = str(uuid.uuid4())
            
            # Store the conversion info
            self.pending_conversions[token] = {
                "file_path": audio_info["file_path"],
                "target_format": target_format.lower(),
                "filename": os.path.splitext(audio_info["filename"])[0] + "." + target_format.lower(),
                "timestamp": datetime.now(),
                "downloaded": False
            }
            
            # Generate HTML with download link and new audio button
            self.output = f"""
            <div class="alert alert-success">
                <h4 class="alert-heading">Konvertierung erfolgreich!</h4>
                <p>Ihre Audiodatei wurde erfolgreich konvertiert. Klicken Sie auf den Button unten, um sie herunterzuladen.</p>
                <hr>
                <div class="d-flex justify-content-between">
                    <a href="/download_audio/{token}" class="btn btn-primary" download>
                        Konvertierte Audiodatei herunterladen
                    </a>
                    <a href="/tool/AudioConverterTool" class="btn btn-secondary">
                        Andere Audiodatei konvertieren
                    </a>
                </div>
            </div>
            """
            
            return True
            
        except Exception as e:
            self.error_message = f"Fehler bei der Konvertierung: {str(e)}"
            return False

    def convert_and_save(self, token):
        """Convert the audio file and return the path to the temporary file."""
        if token not in self.pending_conversions:
            print(f"Error: Token {token} not found in pending conversions")
            return None

        conversion = self.pending_conversions[token]
        if conversion["downloaded"]:
            print(f"Error: File for token {token} was already downloaded")
            return None

        try:
            # Verify source file exists and has content
            if not os.path.exists(conversion["file_path"]):
                print(f"Error: Source file not found: {conversion['file_path']}")
                return None

            if os.path.getsize(conversion["file_path"]) == 0:
                print(f"Error: Source file is empty: {conversion['file_path']}")
                return None

            # Load and convert the audio file
            print(f"Loading audio file: {conversion['file_path']}")
            audio = AudioSegment.from_file(conversion["file_path"])

            # Entferne führenden Punkt (falls vorhanden)
            target_format = conversion["target_format"].lstrip('.')

            # Create output filename in temp directory
            output_path = os.path.join(
                self.temp_dir,
                f"converted_{token}.{target_format}"
            )
            print(f"Converting to: {output_path}")

            # Handle AAC conversion specially
            if target_format == "aac":
                # For AAC, we need to use ffmpeg's AAC encoder directly
                audio.export(output_path, format="adts", parameters=["-c:a", "aac", "-b:a", "192k"])
            else:
                # For other formats, use the standard export
                audio.export(output_path, format=target_format)

            # Verify the file was created and has content
            if not os.path.exists(output_path):
                print(f"Error: Converted file was not created: {output_path}")
                return None

            file_size = os.path.getsize(output_path)
            if file_size == 0:
                print(f"Error: Converted file is empty: {output_path}")
                return None

            print(f"Success: Converted file created with size {file_size} bytes")
            return output_path

        except Exception as e:
            print(f"Error converting audio: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return None


    def cleanup_old_files(self):
        """Remove old conversions and their files."""
        now = datetime.now()
        tokens_to_remove = []
        
        for token, conversion in self.pending_conversions.items():
            # Remove conversions older than 1 hour or already downloaded
            if (now - conversion["timestamp"] > timedelta(hours=1) or 
                conversion["downloaded"]):
                # Try to remove the temporary files
                try:
                    if os.path.exists(conversion["file_path"]):
                        os.remove(conversion["file_path"])
                    
                    converted_path = os.path.join(
                        self.temp_dir,
                        f"converted_{token}.{conversion['target_format']}"
                    )
                    if os.path.exists(converted_path):
                        os.remove(converted_path)
                except Exception as e:
                    print(f"Error cleaning up files: {str(e)}")
                
                tokens_to_remove.append(token)
        
        # Remove the processed tokens from pending_conversions
        for token in tokens_to_remove:
            self.pending_conversions.pop(token, None)