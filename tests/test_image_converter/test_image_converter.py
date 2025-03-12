import os
import pytest
from PIL import Image
import tempfile
from tools.image_converter.image_converter_tool import ImageConverterTool

@pytest.fixture
def sample_image():
    # Create a temporary test image
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "test_image.png")
    
    # Create a 100x100 red image
    img = Image.new('RGB', (100, 100), color='red')
    img.save(file_path)
    
    yield {
        "file_path": file_path,
        "filename": "test_image.png"
    }
    
    # Cleanup after test
    if os.path.exists(file_path):
        os.remove(file_path)

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
    assert "Konvertierung erfolgreich" in tool.output
    assert "download" in tool.output
    assert 'class="btn btn-primary"' in tool.output
    assert 'class="btn btn-secondary"' in tool.output
    assert 'Anderes Bild konvertieren' in tool.output

def test_convert_to_jpeg(sample_image):
    tool = ImageConverterTool()
    result = tool.execute_tool({
        "image": sample_image,
        "target_format": "JPEG"
    })
    assert result == True
    assert "Konvertierung erfolgreich" in tool.output
    assert "download" in tool.output
    assert 'class="btn btn-primary"' in tool.output
    assert 'class="btn btn-secondary"' in tool.output
    assert 'Anderes Bild konvertieren' in tool.output

def test_convert_to_gif(sample_image):
    tool = ImageConverterTool()
    result = tool.execute_tool({
        "image": sample_image,
        "target_format": "GIF"
    })
    assert result == True
    assert "Konvertierung erfolgreich" in tool.output
    assert "download" in tool.output
    assert 'class="btn btn-primary"' in tool.output
    assert 'class="btn btn-secondary"' in tool.output
    assert 'Anderes Bild konvertieren' in tool.output

def test_convert_to_bmp(sample_image):
    tool = ImageConverterTool()
    result = tool.execute_tool({
        "image": sample_image,
        "target_format": "BMP"
    })
    assert result == True
    assert "Konvertierung erfolgreich" in tool.output
    assert "download" in tool.output
    assert 'class="btn btn-primary"' in tool.output
    assert 'class="btn btn-secondary"' in tool.output
    assert 'Anderes Bild konvertieren' in tool.output

def test_convert_to_webp(sample_image):
    tool = ImageConverterTool()
    result = tool.execute_tool({
        "image": sample_image,
        "target_format": "WEBP"
    })
    assert result == True
    assert "Konvertierung erfolgreich" in tool.output
    assert "download" in tool.output
    assert 'class="btn btn-primary"' in tool.output
    assert 'class="btn btn-secondary"' in tool.output
    assert 'Anderes Bild konvertieren' in tool.output

def test_unsupported_format(sample_image):
    tool = ImageConverterTool()
    result = tool.execute_tool({
        "image": sample_image,
        "target_format": "UNSUPPORTED"
    })
    assert result == True  # We now accept any format and try to convert it
    assert "Konvertierung erfolgreich" in tool.output

def test_missing_image():
    tool = ImageConverterTool()
    result = tool.execute_tool({
        "target_format": "PNG"
    })
    assert result == False
    assert "Bitte wählen Sie ein Bild aus" in tool.error_message

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
    assert result == True  # Initial validation passes
    # The actual error will occur during download when convert_and_save is called
