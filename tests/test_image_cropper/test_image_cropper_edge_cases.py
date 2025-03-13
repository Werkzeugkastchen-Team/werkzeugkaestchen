import os
import pytest
import tempfile
from PIL import Image
import json
from tools.image_cropper.image_cropper_tool import ImageCropperTool

@pytest.fixture
def sample_images():
    """Create various test images with different dimensions and characteristics"""
    temp_dir = tempfile.gettempdir()
    images = {}
    
    # Standard test image (100x100)
    standard_path = os.path.join(temp_dir, "standard.png")
    Image.new('RGB', (100, 100), color='red').save(standard_path)
    images['standard'] = {
        "file_path": standard_path,
        "filename": "standard.png",
        "width": 100,
        "height": 100
    }
    
    # Minimum size image (20x20)
    min_path = os.path.join(temp_dir, "minimum.png")
    Image.new('RGB', (20, 20), color='blue').save(min_path)
    images['minimum'] = {
        "file_path": min_path,
        "filename": "minimum.png",
        "width": 20,
        "height": 20
    }
    
    # Very large image (5000x5000)
    large_path = os.path.join(temp_dir, "large.png")
    Image.new('RGB', (5000, 5000), color='green').save(large_path)
    images['large'] = {
        "file_path": large_path,
        "filename": "large.png",
        "width": 5000,
        "height": 5000
    }
    
    # Non-square image (200x100)
    rect_path = os.path.join(temp_dir, "rectangle.png")
    Image.new('RGB', (200, 100), color='yellow').save(rect_path)
    images['rectangle'] = {
        "file_path": rect_path,
        "filename": "rectangle.png",
        "width": 200,
        "height": 100
    }
    
    yield images
    
    # Cleanup after tests
    for img in images.values():
        if os.path.exists(img["file_path"]):
            os.remove(img["file_path"])

def test_minimum_crop_size(sample_images):
    """Test cropping with minimum allowed dimensions (20x20)"""
    tool = ImageCropperTool()
    crop_data = {
        "x": 0,
        "y": 0,
        "width": 20,
        "height": 20
    }
    
    result = tool.execute_tool({
        "image": sample_images['standard'],
        "crop_data": json.dumps(crop_data)
    })
    
    assert result == True
    assert tool.error_message == ""

def test_crop_too_small(sample_images):
    """Test cropping with dimensions smaller than minimum (19x19)"""
    tool = ImageCropperTool()
    crop_data = {
        "x": 0,
        "y": 0,
        "width": 19,
        "height": 19
    }
    
    result = tool.execute_tool({
        "image": sample_images['standard'],
        "crop_data": json.dumps(crop_data)
    })
    
    assert result == False
    assert "zu klein" in tool.error_message

def test_crop_exceeds_boundaries(sample_images):
    """Test cropping with coordinates that exceed image boundaries"""
    tool = ImageCropperTool()
    crop_data = {
        "x": 90,
        "y": 90,
        "width": 20,
        "height": 20
    }
    
    result = tool.execute_tool({
        "image": sample_images['standard'],
        "crop_data": json.dumps(crop_data)
    })
    
    assert result == False
    assert "Bildgrenzen" in tool.error_message

def test_crop_negative_coordinates(sample_images):
    """Test cropping with negative coordinates"""
    tool = ImageCropperTool()
    crop_data = {
        "x": -10,
        "y": -10,
        "width": 50,
        "height": 50
    }
    
    result = tool.execute_tool({
        "image": sample_images['standard'],
        "crop_data": json.dumps(crop_data)
    })
    
    assert result == False
    assert "negativ" in tool.error_message

def test_crop_exact_image_size(sample_images):
    """Test cropping the entire image"""
    tool = ImageCropperTool()
    crop_data = {
        "x": 0,
        "y": 0,
        "width": 100,
        "height": 100
    }
    
    result = tool.execute_tool({
        "image": sample_images['standard'],
        "crop_data": json.dumps(crop_data)
    })
    
    assert result == True
    assert tool.error_message == ""

def test_crop_minimum_size_image(sample_images):
    """Test cropping an image that is exactly minimum size"""
    tool = ImageCropperTool()
    crop_data = {
        "x": 0,
        "y": 0,
        "width": 20,
        "height": 20
    }
    
    result = tool.execute_tool({
        "image": sample_images['minimum'],
        "crop_data": json.dumps(crop_data)
    })
    
    assert result == True
    assert tool.error_message == ""

def test_crop_large_image(sample_images):
    """Test cropping a very large image"""
    tool = ImageCropperTool()
    crop_data = {
        "x": 0,
        "y": 0,
        "width": 1000,
        "height": 1000
    }
    
    result = tool.execute_tool({
        "image": sample_images['large'],
        "crop_data": json.dumps(crop_data)
    })
    
    assert result == True
    assert tool.error_message == ""

def test_crop_non_square_region(sample_images):
    """Test cropping a rectangular region"""
    tool = ImageCropperTool()
    crop_data = {
        "x": 0,
        "y": 0,
        "width": 100,
        "height": 50
    }
    
    result = tool.execute_tool({
        "image": sample_images['rectangle'],
        "crop_data": json.dumps(crop_data)
    })
    
    assert result == True
    assert tool.error_message == ""

def test_invalid_json_crop_data(sample_images):
    """Test handling of invalid JSON in crop data"""
    tool = ImageCropperTool()
    
    result = tool.execute_tool({
        "image": sample_images['standard'],
        "crop_data": "invalid json"
    })
    
    assert result == False
    assert "JSON" in tool.error_message

def test_missing_crop_data(sample_images):
    """Test handling of missing crop data"""
    tool = ImageCropperTool()
    
    result = tool.execute_tool({
        "image": sample_images['standard']
    })
    
    assert result == False
    assert "Zuschnittdaten" in tool.error_message

def test_missing_image(sample_images):
    """Test handling of missing image"""
    tool = ImageCropperTool()
    crop_data = {
        "x": 0,
        "y": 0,
        "width": 50,
        "height": 50
    }
    
    result = tool.execute_tool({
        "crop_data": json.dumps(crop_data)
    })
    
    assert result == False
    assert "Bild" in tool.error_message

def test_cleanup_after_crop(sample_images):
    """Test that temporary files are cleaned up after cropping"""
    tool = ImageCropperTool()
    crop_data = {
        "x": 0,
        "y": 0,
        "width": 50,
        "height": 50
    }
    
    tool.execute_tool({
        "image": sample_images['standard'],
        "crop_data": json.dumps(crop_data)
    })
    
    # Simulate download completion
    for token in tool.pending_crops.keys():
        tool.pending_crops[token]['downloaded'] = True
    
    # Run cleanup
    tool.cleanup_old_files()
    
    # Check that pending_crops is empty
    assert len(tool.pending_crops) == 0 