import os
import pytest
from PIL import Image
import tempfile
from tools.image_converter.image_converter_tool import ImageConverterTool

@pytest.fixture
def sample_image():
    # Create a temporary test image
    img_path = os.path.join(tempfile.gettempdir(), "test_image.png")
    img = Image.new('RGB', (100, 100), color='red')
    img.save(img_path)
    return {
        "file_path": img_path,
        "filename": "test_image.png"
    }

def test_image_converter_initialization():
    tool = ImageConverterTool()
    assert tool.name == "Bildkonverter"
    assert "image" in tool.input_params
    assert "target_format" in tool.input_params

def test_convert_to_png(sample_image):
    tool = ImageConverterTool()
    result = tool.execute_tool({
        "image": sample_image,
        "target_format": "PNG"
    })
    assert result == True
    assert "Das Bild wurde erfolgreich in das Format PNG konvertiert" in tool.output
    assert 'href="/download/' in tool.output
    assert 'class="btn btn-primary"' in tool.output

def test_convert_to_jpeg(sample_image):
    tool = ImageConverterTool()
    result = tool.execute_tool({
        "image": sample_image,
        "target_format": "JPEG"
    })
    assert result == True
    assert "Das Bild wurde erfolgreich in das Format JPEG konvertiert" in tool.output
    assert 'href="/download/' in tool.output
    assert 'class="btn btn-primary"' in tool.output

def test_convert_to_gif(sample_image):
    tool = ImageConverterTool()
    result = tool.execute_tool({
        "image": sample_image,
        "target_format": "GIF"
    })
    assert result == True
    assert "Das Bild wurde erfolgreich in das Format GIF konvertiert" in tool.output
    assert 'href="/download/' in tool.output
    assert 'class="btn btn-primary"' in tool.output

def test_convert_to_bmp(sample_image):
    tool = ImageConverterTool()
    result = tool.execute_tool({
        "image": sample_image,
        "target_format": "BMP"
    })
    assert result == True
    assert "Das Bild wurde erfolgreich in das Format BMP konvertiert" in tool.output
    assert 'href="/download/' in tool.output
    assert 'class="btn btn-primary"' in tool.output

def test_convert_to_webp(sample_image):
    tool = ImageConverterTool()
    result = tool.execute_tool({
        "image": sample_image,
        "target_format": "WEBP"
    })
    assert result == True
    assert "Das Bild wurde erfolgreich in das Format WEBP konvertiert" in tool.output
    assert 'href="/download/' in tool.output
    assert 'class="btn btn-primary"' in tool.output

def test_unsupported_format(sample_image):
    tool = ImageConverterTool()
    result = tool.execute_tool({
        "image": sample_image,
        "target_format": "UNSUPPORTED"
    })
    assert result == False
    assert "wird nicht unterstützt" in tool.error_message

def test_missing_image():
    tool = ImageConverterTool()
    result = tool.execute_tool({
        "target_format": "PNG"
    })
    assert result == False
    assert "Bitte laden Sie ein Bild hoch" in tool.error_message

def test_invalid_image():
    tool = ImageConverterTool()
    invalid_image = {
        "file_path": __file__,  # Use this test file as an invalid image
        "filename": "test.png"
    }
    result = tool.execute_tool({
        "image": invalid_image,
        "target_format": "PNG"
    })
    assert result == False
    assert "konnte nicht als Bild gelesen werden" in tool.error_message
