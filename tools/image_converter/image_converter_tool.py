import os
import tempfile
import uuid
import shutil
from PIL import Image
from tool_interface import MiniTool, OutputType

class ImageConverterTool(MiniTool):
    name = "Bildkonverter"
    description = "Konvertiert Bilder in verschiedene Formate (PNG, JPG, GIF, BMP, WEBP)."
    
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
        super().__init__(self.name, "ImageConverterTool", OutputType.FILE)
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
            if 'image' not in input_params:
                self.error_message = "Bitte laden Sie ein Bild hoch."
                return False
            
            image_data = input_params.get('image')
            target_format = input_params.get('target_format', '').upper()
            
            if target_format not in self.SUPPORTED_FORMATS:
                self.error_message = f"Das Format {target_format} wird nicht unterstützt."
                return False
            
            # Get the uploaded file path
            input_path = image_data.get('file_path')
            original_filename = image_data.get('filename')
            
            try:
                # Open and verify the image
                img = Image.open(input_path)
                self.current_format = img.format
                
                # Don't block JPG to JPEG conversion or vice versa
                # Just ensure the current format is valid
                if self.current_format not in self.SUPPORTED_FORMATS:
                    self.error_message = f"Das Format {self.current_format} wird nicht unterstützt."
                    return False
                
                # Generate a unique token for this conversion
                token = str(uuid.uuid4())
                
                # Create output filename (always use lowercase extension)
                filename_without_ext = os.path.splitext(original_filename)[0]
                output_ext = self.SUPPORTED_FORMATS[target_format]  # This ensures jpg/jpeg are handled correctly
                temp_filename = f"{filename_without_ext}.{output_ext}"
                temp_path = os.path.join(self.temp_dir, f"{token}_{temp_filename}")
                
                # Convert and save to temp location
                if target_format in ['JPEG', 'JPG']:
                    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        background.save(temp_path, 'JPEG', quality=95)
                    else:
                        img.convert('RGB').save(temp_path, 'JPEG', quality=95)
                else:
                    img.save(temp_path, target_format)
                
                # Store conversion information
                self.pending_conversions[token] = {
                    'temp_path': temp_path,
                    'filename': temp_filename,  # Store the clean filename without token
                    'target_format': target_format,
                    'downloaded': False  # Track if file has been downloaded
                }
                
                self.output = f"""
                <div class='card'>
                    <div class='card-body'>
                        <h5>Bereit zum Herunterladen</h5>
                        <p>Das Bild wurde erfolgreich in das Format {target_format} konvertiert.</p>
                        <div class="d-flex justify-content-between">
                            <a href="/download/{token}" class="btn btn-primary" id="downloadBtn">
                                Herunterladen
                            </a>
                            <a href="/tool/ImageConverterTool" class="btn btn-secondary">
                                Anderes Bild konvertieren
                            </a>
                        </div>
                        <div id="downloadStatus" class="mt-2" style="display: none;">
                            <div class="alert alert-info">
                                <span id="downloadMessage">Wird heruntergeladen...</span>
                            </div>
                        </div>
                    </div>
                </div>
                <script>
                document.getElementById('downloadBtn').addEventListener('click', function(e) {{
                    e.preventDefault();
                    const downloadBtn = this;
                    const statusDiv = document.getElementById('downloadStatus');
                    const statusMessage = document.getElementById('downloadMessage');
                    
                    if (downloadBtn.classList.contains('disabled')) return;
                    
                    downloadBtn.classList.add('disabled');
                    statusDiv.style.display = 'block';
                    statusMessage.textContent = 'Wird heruntergeladen...';
                    
                    window.location.href = downloadBtn.href;
                    
                    setTimeout(() => {{
                        downloadBtn.classList.remove('disabled');
                        statusMessage.textContent = 'Download erfolgreich!';
                        setTimeout(() => {{
                            statusDiv.style.display = 'none';
                        }}, 3000);
                    }}, 1000);
                }});
                </script>
                """
                return True
                
            except Exception as e:
                self.error_message = "Die Datei konnte nicht als Bild gelesen werden. Bitte stellen Sie sicher, dass es sich um ein gültiges Bildformat handelt."
                return False
            
        except Exception as e:
            self.error_message = f"Ein Fehler ist aufgetreten: {str(e)}"
            return False
            
    @classmethod
    def convert_and_save(cls, token):
        """Copy the converted file to downloads folder when requested"""
        if token not in cls.pending_conversions:
            return None
            
        conv_data = cls.pending_conversions[token]
        temp_path = conv_data['temp_path']
        filename = conv_data['filename']
        
        if not os.path.exists(temp_path):
            return None
            
        # Copy to downloads folder
        downloads_path = os.path.expanduser("~/Downloads")
        output_path = os.path.join(downloads_path, filename)
        
        # Ensure unique filename in downloads folder
        counter = 1
        base_name, ext = os.path.splitext(filename)
        while os.path.exists(output_path):
            output_path = os.path.join(downloads_path, f"{base_name}_{counter}{ext}")
            counter += 1
        
        return temp_path  # Return the temp path instead of copying
            
    @classmethod
    def cleanup_old_files(cls):
        """Clean up old temporary files"""
        for token, data in list(cls.pending_conversions.items()):
            if data['downloaded']:
                try:
                    os.remove(data['temp_path'])
                    del cls.pending_conversions[token]
                except:
                    pass 