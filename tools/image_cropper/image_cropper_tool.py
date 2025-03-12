from PIL import Image
import os
import tempfile
import uuid
from datetime import datetime, timedelta
from tool_interface import MiniTool, OutputType

class ImageCropperTool(MiniTool):
    name = "Bilder zuschneiden"
    description = "Schneiden Sie Ihre Bilder interaktiv zu. Wählen Sie den gewünschten Bereich mit der Maus aus."
    
    # Store pending crops with their metadata
    pending_crops = {}
    temp_dir = tempfile.gettempdir()
    
    def __init__(self):
        super().__init__(self.name, "ImageCropperTool", OutputType.TEXT)
        self.input_params = {
            "image": "file",
            "crop_data": "string"  # Will contain x, y, width, height as JSON
        }
    
    def execute_tool(self, input_params: dict) -> bool:
        try:
            if "image" not in input_params:
                self.error_message = "Bitte wählen Sie ein Bild aus."
                return False
            
            if "crop_data" not in input_params or not input_params["crop_data"]:
                self.error_message = "Keine Zuschnittdaten erhalten."
                return False
            
            image_info = input_params["image"]
            
            # Validate crop data
            try:
                import json
                crop_data = json.loads(input_params["crop_data"])
                
                # Check for required fields
                required_fields = ["x", "y", "width", "height"]
                if not all(field in crop_data for field in required_fields):
                    self.error_message = "Ungültige Zuschnittdaten: Fehlende Koordinaten oder Dimensionen."
                    return False
                
                # Convert to integers and validate
                x = int(crop_data["x"])
                y = int(crop_data["y"])
                width = int(crop_data["width"])
                height = int(crop_data["height"])
                
                # Check for negative coordinates
                if x < 0 or y < 0:
                    self.error_message = "Die Koordinaten dürfen nicht negativ sein."
                    return False
                
                # Check minimum dimensions (20x20)
                if width < 20 or height < 20:
                    self.error_message = "Der ausgewählte Bereich ist zu klein. Die minimale Größe beträgt 20x20 Pixel."
                    return False
                
                # Open image to check boundaries
                with Image.open(image_info["file_path"]) as img:
                    img_width, img_height = img.size
                    
                    # Check if crop exceeds image boundaries
                    if x + width > img_width or y + height > img_height:
                        self.error_message = "Der ausgewählte Bereich überschreitet die Bildgrenzen."
                        return False
                
            except json.JSONDecodeError:
                self.error_message = "Ungültige JSON-Daten für den Zuschnitt."
                return False
            except ValueError:
                self.error_message = "Ungültige Zahlenformate in den Zuschnittdaten."
                return False
            except Exception as e:
                self.error_message = f"Fehler bei der Validierung der Zuschnittdaten: {str(e)}"
                return False
            
            # Generate a unique token for this crop
            token = str(uuid.uuid4())
            
            # Store the crop information
            self.pending_crops[token] = {
                "file_path": image_info["file_path"],
                "crop_data": input_params["crop_data"],
                "filename": image_info["filename"],
                "timestamp": datetime.now(),
                "downloaded": False
            }
            
            # Generate success message with download link
            self.output = f"""
            <div class="alert alert-success">
                <h4 class="alert-heading">Zuschneiden erfolgreich!</h4>
                <p>Ihr Bild wurde erfolgreich zugeschnitten. Klicken Sie auf den Button unten, um es herunterzuladen.</p>
                <hr>
                <div class="d-flex justify-content-between">
                    <a href="/download_crop/{token}" class="btn btn-primary" download>
                        Zugeschnittenes Bild herunterladen
                    </a>
                    <a href="/tool/ImageCropperTool" class="btn btn-secondary">
                        Anderes Bild zuschneiden
                    </a>
                </div>
            </div>
            """
            
            return True
            
        except Exception as e:
            self.error_message = f"Fehler beim Zuschneiden: {str(e)}"
            return False
    
    def crop_and_save(self, token):
        """Perform the actual cropping operation and save the result."""
        if token not in self.pending_crops:
            return None
            
        crop_info = self.pending_crops[token]
        if crop_info["downloaded"]:
            return None
            
        try:
            # Open the image
            with Image.open(crop_info["file_path"]) as img:
                # Parse crop data
                import json
                crop_data = json.loads(crop_info["crop_data"])
                
                # Perform the crop
                cropped = img.crop((
                    int(crop_data["x"]),
                    int(crop_data["y"]),
                    int(crop_data["x"] + crop_data["width"]),
                    int(crop_data["y"] + crop_data["height"])
                ))
                
                # Save to temporary file
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
        """Remove old crops and their files."""
        now = datetime.now()
        tokens_to_remove = []
        
        for token, crop in self.pending_crops.items():
            # Remove crops older than 1 hour or already downloaded
            if (now - crop["timestamp"] > timedelta(hours=1) or 
                crop["downloaded"]):
                # Try to remove the temporary files
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
        
        # Remove the processed tokens
        for token in tokens_to_remove:
            self.pending_crops.pop(token, None) 