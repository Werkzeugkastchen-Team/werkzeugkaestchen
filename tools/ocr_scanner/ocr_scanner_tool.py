import os
import tempfile
import uuid
import base64
import io
import re
import time
import traceback
import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from tool_interface import MiniTool, OutputType
from flask_babel import lazy_gettext as _

class OcrScannerTool(MiniTool):
    name = _("OCR Scanner")
    description = _("Extrahiert Text aus Bilddateien mittels OCR-Technologie.")

    # Supported image formats
    SUPPORTED_FORMATS = ['PNG', 'JPG', 'JPEG', 'BMP', 'TIFF']
    
    # Supported languages
    LANGUAGES = {
        'deu': _('Deutsch'),
        'eng': _('Englisch'),
        'fra': _('Französisch'),
        'spa': _('Spanisch'),
        'ita': _('Italienisch')
    }

    # Class variable to store pending scans
    pending_scans = {}
    temp_dir = tempfile.gettempdir()
    
    # Constants for resource limits
    MAX_IMAGE_SIZE = (1500, 1500)  # Maximum image dimensions
    MAX_PROCESSING_TIME = 15  # Maximum processing time in seconds
    MAX_BLOCK_COUNT = 1000  # Maximum number of text blocks to process
    MAX_COMPONENT_SIZE = 10000  # Maximum pixels in a connected component
    
    # Cloud OCR API settings - using a free public demo OCR API
    CLOUD_OCR_ENABLED = True  # Set to False to disable cloud OCR
    CLOUD_OCR_API_URL = "https://api.ocr.space/parse/image"
    CLOUD_OCR_API_KEY = "helloworld"  # Free demo key for OCR.space API

    def __init__(self):
        super().__init__(self.name, "OcrScannerTool", OutputType.TEXT)
        self.input_params = {
            "image": "file"
        }
        
        # Try to find Tesseract path if installed
        self.tesseract_path = self.find_tesseract()

    def find_tesseract(self):
        """Try to find the Tesseract executable path"""
        common_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            r'/usr/bin/tesseract',
            r'/usr/local/bin/tesseract'
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        return None

    def execute_tool(self, input_params: dict) -> bool:
        try:
            if "image" not in input_params:
                self.error_message = _("Bitte wählen Sie ein Bild aus.")
                return False

            image_info = input_params["image"]

            # Check if the file is a valid image format
            file_extension = os.path.splitext(image_info["filename"])[1].upper().lstrip('.')
            if file_extension not in self.SUPPORTED_FORMATS and file_extension != 'JPEG':
                self.error_message = _("Das ausgewählte Dateiformat wird nicht unterstützt. Unterstützte Formate: PNG, JPG, BMP, TIFF.")
                return False
                
            # Check if file exists and has content
            if not os.path.exists(image_info["file_path"]) or os.path.getsize(image_info["file_path"]) == 0:
                self.error_message = _("Die ausgewählte Datei ist leer oder beschädigt.")
                return False

            # Generate a unique token for this scan
            token = str(uuid.uuid4())

            # Store the scan info
            self.pending_scans[token] = {
                "file_path": image_info["file_path"],
                "timestamp": datetime.now(),
                "processed": False,
                "filename": image_info["filename"]
            }

            # Process the image and extract text
            text, enhanced_image_base64 = self.process_image(token)
            
            if not text or text.strip() == "":
                text = _("Kein Text konnte im Bild erkannt werden. Versuchen Sie ein Bild mit deutlicherem Text oder stellen Sie sicher, dass das Bild Text enthält.")

            # Get text regions if available
            text_regions = self.pending_scans[token].get("text_regions", [])
            has_text_regions = len(text_regions) > 0
            
            # Create JSON for text regions
            text_regions_json = json.dumps(text_regions)
            
            # Create the output HTML
            success_heading = _("Text aus Bild extrahiert")
            download_button = _("Extrahierten Text herunterladen")
            copy_button = _("Text kopieren")
            new_image_button = _("Anderes Bild scannen")
            enhanced_image_title = _("Optimiertes Bild")

            self.output = f"""
            <div class="card mb-4">
                <div class="card-header bg-success text-white">
                    <h4 class="card-title mb-0">{success_heading}</h4>
                </div>
                <div class="card-body">
                    <div class="form-group">
                        <label for="extractedText">{_("Extrahierter Text")}:</label>
                        <textarea id="extractedText" class="form-control" rows="10" readonly>{text}</textarea>
                    </div>
                    <div class="d-flex justify-content-between mt-3">
                        <button onclick="copyToClipboard()" class="btn btn-primary">
                            <i class="fas fa-copy"></i> {copy_button}
                        </button>
                        <a href="/download_text/{token}" class="btn btn-success" download>
                            <i class="fas fa-download"></i> {download_button}
                        </a>
                        <a href="/tool/OcrScannerTool" class="btn btn-secondary">
                            <i class="fas fa-redo"></i> {new_image_button}
                        </a>
                    </div>
                    
                    <div class="mt-4">
                        <h5>{enhanced_image_title}</h5>
                        <div class="text-center">
                            <img src="data:image/png;base64,{enhanced_image_base64}" 
                                class="img-fluid" 
                                style="max-width: 100%; border: 1px solid #ddd; border-radius: 4px; padding: 5px;" 
                                alt="{_("Optimiertes Bild")}"
                                id="enhancedImage">
                        </div>
                    </div>
                </div>
            </div>
            <script>
            function copyToClipboard() {{
                var textarea = document.getElementById('extractedText');
                textarea.select();
                document.execCommand('copy');
                alert('{_("Text in die Zwischenablage kopiert!")}');
            }}
            </script>
            """
            
            return True

        except Exception as e:
            self.error_message = _("Fehler bei der Bildverarbeitung: %(error)s", error=str(e))
            return False

    def detect_text_blocks(self, image):
        """
        Detect blocks of text in an image and return their bounding boxes.
        Uses multiple methods for more robust detection.
        """
        start_time = time.time()
        
        # Convert to grayscale
        gray = image.convert('L')
        
        # Apply multiple thresholds for better detection
        thresholds = [80, 127, 170]  # Low, medium, high thresholds
        all_blocks = []
        
        for threshold in thresholds:
            # Abort if taking too long
            if time.time() - start_time > self.MAX_PROCESSING_TIME / 3:
                break
                
            # Apply threshold to get binary image
            binary = gray.point(lambda x: 0 if x < threshold else 255, '1')
            
            # Find text blocks using a grid-based approach
            width, height = binary.size
            pixels = binary.load()
            
            grid_size = 10  # Divide image into cells
            grid_width = width // grid_size
            grid_height = height // grid_size
            
            # Find potential text blocks
            text_blocks = []
            for y in range(grid_height):
                row_blocks = []
                current_block = None
                
                for x in range(grid_width):
                    # Check timeout
                    if time.time() - start_time > self.MAX_PROCESSING_TIME / 2:
                        break
                    
                    # Count black pixels in this cell
                    x1, y1 = x * grid_size, y * grid_size
                    x2, y2 = min(x1 + grid_size, width), min(y1 + grid_size, height)
                    
                    black_count = 0
                    total = 0
                    for py in range(y1, y2):
                        for px in range(x1, x2):
                            total += 1
                            if px < width and py < height and pixels[px, py] == 0:
                                black_count += 1
                    
                    # Adaptive threshold based on cell position
                    # More strict in the center (likely text area), less strict at edges
                    center_x, center_y = width/2, height/2
                    dist_from_center = ((x*grid_size - center_x)**2 + (y*grid_size - center_y)**2)**0.5
                    max_dist = ((width/2)**2 + (height/2)**2)**0.5
                    relative_dist = dist_from_center / max_dist
                    
                    # Adjust threshold based on distance from center
                    thresh = 0.1 + 0.3 * relative_dist  # 0.1 near center, up to 0.4 at corners
                    
                    if total > 0 and black_count / total > thresh:
                        if current_block is None:
                            current_block = [x1, y1, x2, y2]
                        else:
                            current_block[2] = x2  # Extend current block
                    else:
                        if current_block is not None:
                            # Save completed block
                            row_blocks.append(tuple(current_block))
                            current_block = None
                
                # Don't forget the last block in the row
                if current_block is not None:
                    row_blocks.append(tuple(current_block))
                
                # Add all blocks from this row
                text_blocks.extend(row_blocks)
                
                # Limit the number of blocks to prevent memory issues
                if len(text_blocks) > self.MAX_BLOCK_COUNT:
                    text_blocks = text_blocks[:self.MAX_BLOCK_COUNT]
                    break
                    
            # Merge overlapping blocks
            all_blocks.extend(text_blocks)
            
        return self.merge_overlapping_blocks(all_blocks)
        
    def merge_overlapping_blocks(self, blocks):
        """Merge overlapping blocks to form larger text regions."""
        if not blocks:
            return []
            
        merged_blocks = []
        blocks = sorted(blocks, key=lambda b: (b[1], b[0]))  # Sort by y then x
        
        current = list(blocks[0])
        
        for block in blocks[1:]:
            # Check if blocks overlap
            if (block[0] <= current[2] and  # x1 of next block <= x2 of current
                block[1] <= current[3] and  # y1 of next block <= y2 of current
                block[2] >= current[0] and  # x2 of next block >= x1 of current
                block[3] >= current[1]):    # y2 of next block >= y1 of current
                
                # Merge blocks
                current[0] = min(current[0], block[0])
                current[1] = min(current[1], block[1])
                current[2] = max(current[2], block[2])
                current[3] = max(current[3], block[3])
            else:
                # No overlap, add current block and start a new one
                merged_blocks.append(tuple(current))
                current = list(block)
                
        # Don't forget the last block
        merged_blocks.append(tuple(current))
        
        return merged_blocks

    def simple_ocr(self, image):
        """
        A simplified OCR implementation that works without external libraries.
        """
        try:
            # Basic visual analysis of the image
            width, height = image.size
            
            # Convert to grayscale and apply contrast
            gray = image.convert('L')
            enhanced = ImageEnhance.Contrast(gray).enhance(2.0)
            
            # Find potential text areas by looking for dark regions
            threshold = 127  # Mid-point threshold
            binary = enhanced.point(lambda x: 0 if x < threshold else 255, '1')
            
            # Count dark pixels in a grid
            grid_size = 20
            grid_width = width // grid_size
            grid_height = height // grid_size
            
            # Create a simple visual representation
            grid_text = []
            for y in range(grid_height):
                line = []
                for x in range(grid_width):
                    # Get the region
                    x1, y1 = x * grid_size, y * grid_size
                    x2, y2 = min(x1 + grid_size, width), min(y1 + grid_size, height)
                    region = binary.crop((x1, y1, x2, y2))
                    
                    # Count black pixels
                    black_pixels = sum(1 for pixel in region.getdata() if pixel == 0)
                    total_pixels = (x2-x1) * (y2-y1)
                    
                    # Determine character to use
                    if total_pixels > 0 and black_pixels / total_pixels > 0.3:
                        line.append('█')
                    elif total_pixels > 0 and black_pixels / total_pixels > 0.1:
                        line.append('▓')
                    else:
                        line.append(' ')
                        
                # Add the line if it contains potential text
                if '█' in line or '▓' in line:
                    grid_text.append(''.join(line))
            
            # Only display lines with text-like content
            filtered_lines = [line for line in grid_text if '█' in line or '▓' in line]
            
            if filtered_lines:
                result = "\n".join(filtered_lines)
                return _("Mögliche Textbereiche erkannt:\n\n") + result + "\n\n" + \
                      _("Für eine vollständige Texterkennung empfehlen wir die Installation von Tesseract OCR.")
            else:
                return _("Es wurden keine Textbereiche im Bild erkannt.")
                
        except Exception as e:
            print(f"Error in simple_ocr: {str(e)}")
            traceback.print_exc()
            return _("Der einfache OCR-Algorithmus konnte nicht durchgeführt werden.")

    def process_image(self, token):
        """Process the image to enhance text visibility and attempt OCR if available."""
        if token not in self.pending_scans:
            return None, None

        scan_info = self.pending_scans[token]
        start_time = time.time()
        
        try:
            print(f"Processing image: {scan_info['file_path']}")
            
            # Verify file exists and can be opened
            if not os.path.exists(scan_info["file_path"]):
                print("File does not exist")
                return _("Das Bild konnte nicht gefunden werden."), self.generate_fallback_image()
                
            try:
                # Open the image with error handling
                image = Image.open(scan_info["file_path"])
                
                # Perform a simple operation to verify image is valid
                image_size = image.size
                print(f"Image dimensions: {image_size}")
                
                # Convert to RGB if necessary
                if image.mode not in ('RGB', 'L'):
                    image = image.convert('RGB')
                    
            except Exception as e:
                print(f"Error opening image: {str(e)}")
                traceback.print_exc()
                return _("Das Bild konnte nicht geöffnet werden. Es könnte beschädigt sein."), self.generate_fallback_image()
            
            # Process the image safely
            try:
                # Basic processing steps
                
                # 1. Resize large images to reasonable dimensions
                width, height = image.size
                if width > self.MAX_IMAGE_SIZE[0] or height > self.MAX_IMAGE_SIZE[1]:
                    ratio = min(self.MAX_IMAGE_SIZE[0] / width, self.MAX_IMAGE_SIZE[1] / height)
                    new_size = (int(width * ratio), int(height * ratio))
                    image = image.resize(new_size, Image.LANCZOS)
                
                # 2. Convert to grayscale for OCR processing
                grayscale = image.convert('L')
                
                # 3. Create a copy for display with basic enhancements
                display_image = grayscale.copy()
                display_image = ImageEnhance.Contrast(display_image).enhance(1.8)
                
                # Generate base64 of the enhanced image for display
                buffered = io.BytesIO()
                display_image.save(buffered, format="PNG")
                enhanced_image_base64 = base64.b64encode(buffered.getvalue()).decode()
                
                # Store original image size for text area mapping
                image_width, image_height = image.size
                
                # Try to extract text in order of reliability:
                # 1. Local Tesseract if available
                # 2. Cloud OCR API if enabled
                # 3. Simple OCR as last resort
                extracted_text = ""
                text_regions = []
                
                # Try local Tesseract first if available
                if self.tesseract_path:
                    try:
                        print("Trying local Tesseract OCR")
                        import pytesseract
                        
                        # Set Tesseract path explicitly if we found it
                        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path
                        
                        # Apply basic processing for OCR
                        ocr_image = ImageEnhance.Contrast(grayscale).enhance(1.5)
                        ocr_image = ocr_image.filter(ImageFilter.SHARPEN)
                        
                        # Extract text using pytesseract with detailed output
                        # This gives us word regions and their coordinates
                        ocr_data = pytesseract.image_to_data(ocr_image, output_type=pytesseract.Output.DICT)
                        
                        # Build text regions from OCR data
                        result_text = []
                        for i in range(len(ocr_data['text'])):
                            if int(ocr_data['conf'][i]) > 20 and ocr_data['text'][i].strip():  # Only keep confident results
                                x, y, w, h = ocr_data['left'][i], ocr_data['top'][i], ocr_data['width'][i], ocr_data['height'][i]
                                text = ocr_data['text'][i]
                                result_text.append(text)
                                text_regions.append({
                                    'text': text,
                                    'x': x,
                                    'y': y,
                                    'width': w,
                                    'height': h
                                })
                        
                        # Join all text parts
                        extracted_text = ' '.join(result_text)
                        
                        # If that failed, try standard OCR
                        if not extracted_text.strip():
                            extracted_text = pytesseract.image_to_string(ocr_image)
                            
                            # If still no results, try with original image
                            if not extracted_text.strip():
                                extracted_text = pytesseract.image_to_string(image)
                        
                        # Clean up the text
                        extracted_text = self.clean_text(extracted_text)
                        
                        if extracted_text.strip():
                            print("Local Tesseract extraction successful")
                    
                    except (ImportError, Exception) as e:
                        print(f"Local Tesseract error: {str(e)}")
                        extracted_text = ""
                
                # If local Tesseract failed or isn't available, try cloud OCR
                if not extracted_text.strip() and self.CLOUD_OCR_ENABLED:
                    try:
                        print("Trying cloud OCR service")
                        # Save image to a temporary file for upload
                        buffered = io.BytesIO()
                        image.save(buffered, format="PNG")
                        img_str = base64.b64encode(buffered.getvalue()).decode()
                        
                        # Try to extract text using cloud OCR API
                        cloud_text, cloud_regions = self.extract_text_from_cloud(img_str)
                        if cloud_text:
                            extracted_text = cloud_text
                            text_regions = cloud_regions
                            print("Cloud OCR extraction successful")
                        
                    except Exception as e:
                        print(f"Cloud OCR error: {str(e)}")
                        extracted_text = ""
                
                # If both methods failed, use simple OCR
                if not extracted_text.strip():
                    print("Falling back to simple OCR")
                    extracted_text = self.simple_ocr(image)
                    # No text regions for simple OCR
                
                # Mark as processed and store the results
                self.pending_scans[token]["processed"] = True
                self.pending_scans[token]["extracted_text"] = extracted_text
                self.pending_scans[token]["enhanced_image"] = enhanced_image_base64
                self.pending_scans[token]["text_regions"] = text_regions
                self.pending_scans[token]["image_width"] = image_width
                self.pending_scans[token]["image_height"] = image_height
                
                if not extracted_text.strip():
                    extracted_text = self.generate_fallback_text(image)
                
                return extracted_text, enhanced_image_base64
                
            except Exception as e:
                print(f"Error during image processing: {str(e)}")
                traceback.print_exc()
                return _("Das Bild konnte nicht verarbeitet werden. Bitte versuchen Sie es mit einem anderen Bild."), self.generate_fallback_image()
                
        except Exception as e:
            print(f"Error in process_image: {str(e)}")
            traceback.print_exc()
            return _("Unerwarteter Fehler bei der Bildverarbeitung."), self.generate_fallback_image()

    def extract_text_from_cloud(self, base64_image):
        """Extract text from image using a cloud OCR service"""
        try:
            # Prepare the request data for OCR.space API
            payload = {
                'base64Image': f'data:image/png;base64,{base64_image}',
                'language': 'ger',  # Default language is German
                'OCREngine': '2',   # More accurate OCR engine
                'scale': 'true',    # Improve OCR accuracy by scaling
                'isOverlayRequired': 'true',  # Get word positions
                'detectOrientation': 'true'   # Auto-detect orientation
            }
            
            # Create request headers
            headers = {
                'apikey': self.CLOUD_OCR_API_KEY,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            # Convert payload to URL encoded format
            data = urllib.parse.urlencode(payload).encode('utf-8')
            
            # Create and send request with timeout
            request = urllib.request.Request(
                self.CLOUD_OCR_API_URL,
                data=data,
                headers=headers,
                method='POST'
            )
            
            with urllib.request.urlopen(request, timeout=10) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                
                # Check if OCR was successful
                if response_data.get('IsErroredOnProcessing', True) == False:
                    parsed_results = response_data.get('ParsedResults', [])
                    if parsed_results:
                        # Get the extracted text
                        text = parsed_results[0].get('ParsedText', '')
                        text_overlay = parsed_results[0].get('TextOverlay', {})
                        
                        # Extract text regions if available
                        text_regions = []
                        lines = text_overlay.get('Lines', [])
                        for line in lines:
                            words = line.get('Words', [])
                            for word in words:
                                if 'WordText' in word and 'Left' in word and 'Top' in word and 'Width' in word and 'Height' in word:
                                    text_regions.append({
                                        'text': word['WordText'],
                                        'x': word['Left'],
                                        'y': word['Top'],
                                        'width': word['Width'],
                                        'height': word['Height']
                                    })
                        
                        return self.clean_text(text), text_regions
            
            return "", []
            
        except urllib.error.URLError as e:
            print(f"Cloud OCR connection error: {str(e)}")
            return "", []
        except json.JSONDecodeError as e:
            print(f"Cloud OCR JSON parsing error: {str(e)}")
            return "", []
        except Exception as e:
            print(f"Cloud OCR unexpected error: {str(e)}")
            return "", []

    def generate_fallback_image(self):
        """Generate a placeholder image when the processing fails."""
        try:
            # Create a simple gray image with text
            placeholder = Image.new('RGB', (400, 200), color=(245, 245, 245))
            buffered = io.BytesIO()
            placeholder.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode()
        except:
            # Return an empty string if even this fails
            return ""
            
    def generate_fallback_text(self, image):
        """Generate basic text about the image when OCR fails."""
        try:
            width, height = image.size
            return _("Das Bild hat die Dimensionen %(width)dx%(height)d Pixel. Es wurden keine Textelemente identifiziert.", width=width, height=height)
        except:
            return _("Die Bildinformationen konnten nicht ausgelesen werden.")

    def clean_text(self, text):
        """Clean up the extracted text."""
        if not text:
            return ""
            
        try:
            # Apply a time limit to regex operations
            max_length = 10000  # Limit text size for processing
            if len(text) > max_length:
                text = text[:max_length]  # Truncate very long text
                
            # Remove excessive whitespace
            text = re.sub(r'\s+', ' ', text)
            
            # Remove non-printable characters
            text = ''.join(c for c in text if c.isprintable() or c in ['\n', '\t'])
            
            # Clean up line breaks (but preserve paragraph structure)
            text = re.sub(r'\n{3,}', '\n\n', text)  # Reduce multiple blank lines to one
            
            # Remove isolated punctuation lines
            text = re.sub(r'^\s*[^\w\s]+\s*$', '', text, flags=re.MULTILINE)
            
            # Fix common OCR errors
            text = text.replace('l.', 'i.')  # Common OCR confusion
            text = text.replace('|', 'I')    # Pipe to I
            
            return text.strip()
        except Exception as e:
            print(f"Error cleaning text: {str(e)}")
            return text or ""

    def get_extracted_text(self, token):
        """Returns the extracted text for downloading."""
        if token not in self.pending_scans:
            return _("Text nicht gefunden.")
            
        scan_info = self.pending_scans[token]
        
        # If text hasn't been extracted yet, extract it now
        if "extracted_text" not in scan_info:
            text, _ = self.process_image(token)
            return text or _("Keine Textelemente gefunden.")
            
        return scan_info["extracted_text"] or _("Keine Textelemente gefunden.")

    def cleanup_old_files(self):
        """Remove old scans and their files."""
        now = datetime.now()
        tokens_to_remove = []

        for token, scan in self.pending_scans.items():
            # Remove scans older than 1 hour
            if now - scan["timestamp"] > timedelta(hours=1):
                # Try to remove the temporary files
                try:
                    if os.path.exists(scan["file_path"]):
                        os.remove(scan["file_path"])
                except Exception as e:
                    print(f"Error cleaning up files: {str(e)}")

                tokens_to_remove.append(token)

        # Remove the processed tokens from pending_scans
        for token in tokens_to_remove:
            self.pending_scans.pop(token, None) 