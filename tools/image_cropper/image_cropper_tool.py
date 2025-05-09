from flask_babel import lazy_gettext as _
from PIL import Image
import os
import tempfile
import uuid
from datetime import datetime, timedelta
from tool_interface import MiniTool, OutputType
import json

class ImageCropperTool(MiniTool):
    name = _("Bilder zuschneiden")
    description = _("Schneiden Sie Ihre Bilder interaktiv zu. Wählen Sie den gewünschten Bereich mit der Maus aus.")

    # Speichert ausstehende Zuschnitte mit Metadaten
    pending_crops = {}
    temp_dir = tempfile.gettempdir()

    def __init__(self):
        super().__init__(self.name, "ImageCropperTool", OutputType.TEXT)
        self.input_params = {
            "image": "file",
            "crop_data": "string"  # Enthält x, y, width, height als JSON
        }

    def execute_tool(self, input_params: dict) -> bool:
        try:
            if "image" not in input_params:
                self.error_message = _("Bitte wählen Sie ein Bild aus.")
                return False

            if "crop_data" not in input_params or not input_params["crop_data"]:
                self.error_message = _("Keine Zuschnittdaten erhalten.")
                return False

            image_info = input_params["image"]

            # Validierung der Zuschnittdaten
            try:
                crop_data = json.loads(input_params["crop_data"])

                # Überprüfe erforderliche Felder
                required_fields = ["x", "y", "width", "height"]
                if not all(field in crop_data for field in required_fields):
                    self.error_message = _("Ungültige Zuschnittdaten: Fehlende Koordinaten oder Dimensionen.")
                    return False

                # Umwandlung in Integer und Validierung
                x = int(crop_data["x"])
                y = int(crop_data["y"])
                width = int(crop_data["width"])
                height = int(crop_data["height"])

                # Negative Koordinaten überprüfen
                if x < 0 or y < 0:
                    self.error_message = _("Die Koordinaten dürfen nicht negativ sein.")
                    return False

                # Mindestdimensionen (20x20) prüfen
                if width < 20 or height < 20:
                    self.error_message = _("Der ausgewählte Bereich ist zu klein. Die minimale Größe beträgt 20x20 Pixel.")
                    return False

                # Bildgrenzen prüfen
                with Image.open(image_info["file_path"]) as img:
                    img_width, img_height = img.size
                    if x + width > img_width or y + height > img_height:
                        self.error_message = _("Der ausgewählte Bereich überschreitet die Bildgrenzen.")
                        return False

            except json.JSONDecodeError:
                self.error_message = _("Ungültige JSON-Daten für den Zuschnitt.")
                return False
            except ValueError:
                self.error_message = _("Ungültige Zahlenformate in den Zuschnittdaten.")
                return False
            except Exception as e:
                self.error_message = _("Fehler bei der Validierung der Zuschnittdaten: ") + str(e)
                return False

            # Erzeuge ein eindeutiges Token für diesen Zuschnitt
            token = str(uuid.uuid4())

            # Speichere die Zuschnitt-Informationen
            self.pending_crops[token] = {
                "file_path": image_info["file_path"],
                "crop_data": input_params["crop_data"],
                "filename": image_info["filename"],
                "timestamp": datetime.now(),
                "downloaded": False
            }

            # Variablen für übersetzte Texte definieren
            success_heading = _("Zuschneiden erfolgreich!")
            success_message = _(
                "Ihr Bild wurde erfolgreich zugeschnitten. Klicken Sie auf den Button unten, um es herunterzuladen.")
            download_img_text = _("Zugeschnittenes Bild herunterladen")
            another_img_text = _("Anderes Bild zuschneiden")

            html_output = f"""
                            <div class=\"alert alert-success\">
                                <h4 class=\"alert-heading\">{success_heading}</h4>
                                <p>{success_message}</p>
                                <hr>
                                <div class=\"d-flex justify-content-between\">
                                    <a href=\"/download_crop/{token}\" class=\"btn btn-primary\" download>
                                        {download_img_text}
                                    </a>
                                    <a href=\"/tool/ImageCropperTool\" class=\"btn btn-secondary\">
                                        {another_img_text}
                                    </a>
                                </div>
                            </div>
                            """
            self.output = html_output.format(token=token)
            return True



        except Exception as e:
            self.error_message = _("Fehler beim Zuschneiden: ") + str(e)
            return False

    def crop_and_save(self, token):
        """Führt den eigentlichen Zuschnitt durch und speichert das Ergebnis."""
        if token not in self.pending_crops:
            return None

        crop_info = self.pending_crops[token]
        if crop_info["downloaded"]:
            return None

        try:
            with Image.open(crop_info["file_path"]) as img:
                crop_data = json.loads(crop_info["crop_data"])
                cropped = img.crop((
                    int(crop_data["x"]),
                    int(crop_data["y"]),
                    int(crop_data["x"]) + int(crop_data["width"]),
                    int(crop_data["y"]) + int(crop_data["height"])
                ))
                output_path = os.path.join(
                    self.temp_dir,
                    f"cropped_{token}_{crop_info['filename']}"
                )
                cropped.save(output_path)
                return output_path

        except Exception as e:
            print(f"Error cropping image: {str(e)}")
            return None

    def cleanup_old_files(self):
        """Entfernt alte Zuschnitte und deren Dateien."""
        now = datetime.now()
        tokens_to_remove = []

        for token, crop in self.pending_crops.items():
            if (now - crop["timestamp"] > timedelta(hours=1)) or crop["downloaded"]:
                try:
                    if os.path.exists(crop["file_path"]):
                        os.remove(crop["file_path"])
                    cropped_path = os.path.join(
                        self.temp_dir,
                        f"cropped_{token}_{crop['filename']}"
                    )
                    if os.path.exists(cropped_path):
                        os.remove(cropped_path)
                except Exception as e:
                    print(f"Error cleaning up files: {str(e)}")
                tokens_to_remove.append(token)

        for token in tokens_to_remove:
            self.pending_crops.pop(token, None)