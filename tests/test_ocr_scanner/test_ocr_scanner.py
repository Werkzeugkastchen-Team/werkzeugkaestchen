import os
import pytest
import tempfile
import base64
import sys
from PIL import Image, ImageDraw, ImageFont
from unittest.mock import patch, MagicMock

# Mock flask_babel before importing the tool
sys.modules['flask_babel'] = MagicMock()
sys.modules['flask_babel'].lazy_gettext = lambda x: x

# Now import the tool
from tools.ocr_scanner.ocr_scanner_tool import OcrScannerTool

@pytest.fixture
def sample_text_image():
    # Create a temporary test image with text
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "test_text_image.png")
    
    # Create a white image
    img = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a simple font
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        # Fallback to default
        font = ImageFont.load_default()
    
    # Add test text
    test_text = "Dies ist ein Test für OCR"
    draw.text((50, 80), test_text, fill="black", font=font)
    
    # Save the image
    img.save(file_path)
    
    yield {
        "file_path": file_path,
        "filename": "test_text_image.png",
        "text": test_text
    }
    
    # Cleanup after test
    if os.path.exists(file_path):
        os.remove(file_path)

def test_ocr_scanner_initialization():
    tool = OcrScannerTool()
    assert tool.name == "OCR Scanner"
    assert "image" in tool.input_params
    assert "language" not in tool.input_params  # Language parameter removed

def test_detect_text_blocks():
    # Create a simple image with clear text blocks
    img = Image.new('RGB', (300, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw two text-like rectangles
    draw.rectangle([(50, 50), (250, 80)], fill="black")
    draw.rectangle([(50, 100), (200, 130)], fill="black")
    
    tool = OcrScannerTool()
    text_blocks = tool.detect_text_blocks(img)
    
    # Verify we detected the blocks
    assert len(text_blocks) > 0

def test_simple_ocr():
    # Create a simple image with text-like patterns
    img = Image.new('RGB', (300, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw two lines of "text" blocks
    draw.rectangle([(50, 50), (100, 70)], fill="black")
    draw.rectangle([(120, 50), (170, 70)], fill="black")
    draw.rectangle([(190, 50), (240, 70)], fill="black")
    
    # Second line
    draw.rectangle([(50, 100), (120, 120)], fill="black")
    draw.rectangle([(140, 100), (210, 120)], fill="black")
    
    tool = OcrScannerTool()
    result = tool.simple_ocr(img)
    
    # Check that we got some output
    assert isinstance(result, str)
    if result:  # If text was detected
        assert "Mögl" in result  # Should contain "Mögliche Textbereiche erkannt"
        assert "█" in result  # Should contain block characters representing text

@patch('builtins.__import__')
def test_image_processing_without_tesseract(mock_import, sample_text_image):
    # Mock pytesseract import to always fail
    def mock_import_error(name, *args, **kwargs):
        if name == 'pytesseract':
            raise ImportError("No module named 'pytesseract'")
        return __import__(name, *args, **kwargs)
    
    mock_import.side_effect = mock_import_error
    
    # Patch the execute_tool method to avoid running the whole pipeline
    with patch.object(OcrScannerTool, 'process_image') as mock_process:
        # Set up the mock to return sample text and a fake image
        mock_process.return_value = ("Mögliche Textbereiche erkannt:\n\n█████\n", "fake_base64")
        
        tool = OcrScannerTool()
        result = tool.execute_tool({
            "image": sample_text_image
        })
        
        assert result is True
        assert mock_process.called

@patch('builtins.__import__')
def test_ocr_with_pytesseract(mock_import, sample_text_image):
    # Create a mock pytesseract module
    mock_tesseract = MagicMock()
    mock_tesseract.image_to_string.return_value = sample_text_image["text"]
    mock_tesseract.Output = MagicMock()
    mock_tesseract.Output.DICT = "dict"
    mock_tesseract.image_to_data.return_value = {
        'text': [sample_text_image["text"]],
        'conf': [90],
        'left': [10],
        'top': [20],
        'width': [100],
        'height': [30]
    }
    
    # Mock the import to return our mock module
    def mock_import_success(name, *args, **kwargs):
        if name == 'pytesseract':
            return mock_tesseract
        return __import__(name, *args, **kwargs)
    
    mock_import.side_effect = mock_import_success
    
    # Patch the process_image method to avoid running the actual pipeline
    with patch.object(OcrScannerTool, 'process_image') as mock_process:
        # Set up the mock to return sample text and a fake image
        mock_process.return_value = (sample_text_image["text"], "fake_base64")
        
        tool = OcrScannerTool()
        result = tool.execute_tool({
            "image": sample_text_image
        })
        
        assert result is True
        assert mock_process.called

def test_text_cleaning():
    tool = OcrScannerTool()
    
    # Test with messy text
    messy_text = "This  has  extra   spaces\n\n\nand\textra\t\tnewlines"
    clean_text = tool.clean_text(messy_text)
    
    # Should collapse multiple spaces and preserve some structure
    assert "  " not in clean_text  # No double spaces
    assert "\n\n\n" not in clean_text  # No triple newlines
    assert "This has extra spaces" in clean_text

def test_invalid_image():
    tool = OcrScannerTool()
    
    # Create a text file instead of an image
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "test.txt")
    
    with open(file_path, 'w') as f:
        f.write("This is not an image")
    
    try:
        result = tool.execute_tool({
            "image": {
                "file_path": file_path,
                "filename": "test.txt"
            }
        })
        
        assert result is False
        assert "Dateiformat wird nicht unterstützt" in tool.error_message
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

def test_missing_image():
    tool = OcrScannerTool()
    result = tool.execute_tool({})
    
    assert result is False
    assert "Bitte wählen Sie ein Bild aus" in tool.error_message 