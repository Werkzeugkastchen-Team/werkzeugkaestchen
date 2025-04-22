import os
import tempfile
import uuid
from PIL import Image
from tool_interface import MiniTool, OutputType
from datetime import datetime, timedelta
from flask_babel import lazy_gettext as _


class ImageConverterTool(MiniTool):
    name = _("Bildkonverter")
    description = _("Konvertiert Bilder in verschiedene Formate (PNG, JPG, GIF, BMP, WEBP).")

    SUPPORTED_FORMATS = {
        'PNG': 'png',
        'JPEG': 'jpeg',
        'JPG': 'jpeg',  # Add JPG as equivalent to JPEG
        'GIF': 'gif',
        'BMP': 'bmp',
        'WEBP': 'webp'
    }

    # Add format display names mapping
    FORMAT_DISPLAY = {
        'JPEG': 'JPEG',
        'JPG': 'JPG',
        'PNG': 'PNG',
        'GIF': 'GIF',
        'BMP': 'BMP',
        'WEBP': 'WEBP'
    }

    # Class variable to store pending conversions
    pending_conversions = {}
    temp_dir = tempfile.gettempdir()  # Get system's temp directory

    def __init__(self):
        super().__init__(self.name, "ImageConverterTool", OutputType.TEXT)
        self.input_params = {
            "image": "file",
            "target_format": "string"
        }
        self.current_format = None

    def get_available_formats(self):
        """Returns list of available formats excluding the current format"""
        if not self.current_format:
            return ['PNG', 'JPG', 'GIF', 'BMP', 'WEBP']  # Show JPG instead of JPEG
        formats = ['PNG', 'JPG', 'GIF', 'BMP', 'WEBP']  # Standard format list with JPG
        # Only remove the current format's display name
        current_display = self.FORMAT_DISPLAY.get(self.current_format, self.current_format)
        if current_display in formats:
            formats.remove(current_display)
        return formats

    def execute_tool(self, input_params: dict) -> bool:
        try:
            if "image" not in input_params:
                self.error_message = _("Bitte wählen Sie ein Bild aus.")
                return False

            image_info = input_params["image"]
            target_format = input_params.get("target_format")

            if not target_format:
                self.error_message = _("Bitte wählen Sie ein Zielformat aus.")
                return False

            # Generate a unique token for this conversion
            token = str(uuid.uuid4())

            # Store the conversion info
            self.pending_conversions[token] = {
                "file_path": image_info["file_path"],
                "target_format": target_format.lower(),
                "filename": os.path.splitext(image_info["filename"])[0] + "." + target_format.lower(),
                "timestamp": datetime.now(),
                "downloaded": False
            }

            # Definiere die Texte für die Übersetzung
            success_heading = _("Konvertierung erfolgreich!")
            success_message = _(
                "Ihr Bild wurde erfolgreich konvertiert. Klicken Sie auf den Button unten, um es herunterzuladen.")
            download_button = _("Konvertiertes Bild herunterladen")
            new_image_button = _("Anderes Bild konvertieren")

            # Generate HTML with download link and new image button
            self.output = f"""
            <div class="alert alert-success">
                <h4 class="alert-heading">{success_heading}</h4>
                <p>{success_message}</p>
                <hr>
                <div class="d-flex justify-content-between">
                    <a href="/download/{token}" class="btn btn-primary" download>
                        {download_button}
                    </a>
                    <a href="/tool/ImageConverterTool" class="btn btn-secondary">
                        {new_image_button}
                    </a>
                </div>
            </div>
            """

            return True

        except Exception as e:
            self.error_message = _("Fehler bei der Konvertierung: %(error)s", error=str(e))
            return False

    def convert_and_save(self, token):
        """Convert the image and return the path to the temporary file."""
        if token not in self.pending_conversions:
            return None

        conversion = self.pending_conversions[token]
        if conversion["downloaded"]:
            return None

        try:
            # Open and convert the image
            with Image.open(conversion["file_path"]) as img:
                # Create output filename in temp directory
                output_path = os.path.join(
                    self.temp_dir,
                    f"converted_{token}.{conversion['target_format']}"
                )

                # Convert and save
                if conversion["target_format"].upper() == "JPEG":
                    # Convert to RGB if saving as JPEG
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")

                img.save(output_path, format=conversion["target_format"].upper())
                return output_path

        except Exception as e:
            print(f"Error converting image: {str(e)}")
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