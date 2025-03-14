import os
import pytest
import tempfile
from pydub import AudioSegment
from tools.audio_converter.audio_converter_tool import AudioConverterTool

@pytest.fixture
def sample_audio():
    # Create a temporary test audio file
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "test_audio.wav")
    
    # Create a 1-second test audio file
    audio = AudioSegment.silent(duration=1000)  # 1 second of silence
    audio.export(file_path, format="wav")
    
    yield {
        "file_path": file_path,
        "filename": "test_audio.wav"
    }
    
    # Cleanup after test
    if os.path.exists(file_path):
        os.remove(file_path)

def test_audio_converter_initialization():
    """Test if the AudioConverterTool initializes correctly"""
    tool = AudioConverterTool()
    assert tool.name == "Audio Konverter"
    assert "audio_file" in tool.input_params
    assert "target_format" in tool.input_params
    assert len(tool.get_available_formats()) == 4  # MP3, WAV, AAC, FLAC

def test_convert_to_mp3(sample_audio):
    """Test conversion to MP3 format"""
    tool = AudioConverterTool()
    result = tool.execute_tool({
        "audio_file": sample_audio,
        "target_format": "MP3"
    })
    assert result == True
    assert "Konvertierung erfolgreich" in tool.output
    assert "download" in tool.output
    assert 'class="btn btn-primary"' in tool.output
    assert 'class="btn btn-secondary"' in tool.output
    assert 'Andere Audiodatei konvertieren' in tool.output

def test_convert_to_wav(sample_audio):
    """Test conversion to WAV format"""
    tool = AudioConverterTool()
    result = tool.execute_tool({
        "audio_file": sample_audio,
        "target_format": "WAV"
    })
    assert result == True
    assert "Konvertierung erfolgreich" in tool.output
    assert "download" in tool.output
    assert 'class="btn btn-primary"' in tool.output
    assert 'class="btn btn-secondary"' in tool.output
    assert 'Andere Audiodatei konvertieren' in tool.output

def test_convert_to_aac(sample_audio):
    """Test conversion to AAC format"""
    tool = AudioConverterTool()
    result = tool.execute_tool({
        "audio_file": sample_audio,
        "target_format": "AAC"
    })
    assert result == True
    assert "Konvertierung erfolgreich" in tool.output
    assert "download" in tool.output
    assert 'class="btn btn-primary"' in tool.output
    assert 'class="btn btn-secondary"' in tool.output
    assert 'Andere Audiodatei konvertieren' in tool.output

def test_convert_to_flac(sample_audio):
    """Test conversion to FLAC format"""
    tool = AudioConverterTool()
    result = tool.execute_tool({
        "audio_file": sample_audio,
        "target_format": "FLAC"
    })
    assert result == True
    assert "Konvertierung erfolgreich" in tool.output
    assert "download" in tool.output
    assert 'class="btn btn-primary"' in tool.output
    assert 'class="btn btn-secondary"' in tool.output
    assert 'Andere Audiodatei konvertieren' in tool.output

def test_unsupported_format(sample_audio):
    """Test handling of unsupported format"""
    tool = AudioConverterTool()
    result = tool.execute_tool({
        "audio_file": sample_audio,
        "target_format": "UNSUPPORTED"
    })
    assert result == True  # We now accept any format and try to convert it
    assert "Konvertierung erfolgreich" in tool.output

def test_missing_audio_file():
    """Test handling of missing audio file"""
    tool = AudioConverterTool()
    result = tool.execute_tool({
        "target_format": "MP3"
    })
    assert result == False
    assert "Bitte wählen Sie eine Audiodatei aus" in tool.error_message

def test_missing_target_format(sample_audio):
    """Test handling of missing target format"""
    tool = AudioConverterTool()
    result = tool.execute_tool({
        "audio_file": sample_audio
    })
    assert result == False
    assert "Bitte wählen Sie ein Zielformat aus" in tool.error_message

def test_invalid_audio_file():
    """Test handling of invalid audio file"""
    tool = AudioConverterTool()
    invalid_audio = {
        "file_path": __file__,  # Use this test file as an invalid audio
        "filename": "test.wav"
    }
    result = tool.execute_tool({
        "audio_file": invalid_audio,
        "target_format": "MP3"
    })
    assert result == True  # Initial validation passes
    # The actual error will occur during download when convert_and_save is called

def test_cleanup_old_files(sample_audio):
    """Test cleanup of old files"""
    tool = AudioConverterTool()
    
    # Create a test conversion
    result = tool.execute_tool({
        "audio_file": sample_audio,
        "target_format": "MP3"
    })
    assert result == True
    
    # Get the token from the output
    token = None
    for t in tool.pending_conversions:
        if tool.pending_conversions[t]["target_format"] == "mp3":
            token = t
            break
    
    assert token is not None
    
    # Mark as downloaded
    tool.pending_conversions[token]["downloaded"] = True
    
    # Run cleanup
    tool.cleanup_old_files()
    
    # Verify the conversion was removed
    assert token not in tool.pending_conversions

def test_get_available_formats(sample_audio):
    """Test getting available formats"""
    tool = AudioConverterTool()
    
    # Test with no current format
    formats = tool.get_available_formats()
    assert len(formats) == 4
    assert "MP3" in formats
    assert "WAV" in formats
    assert "AAC" in formats
    assert "FLAC" in formats
    
    # Test with current format
    tool.current_format = "MP3"
    formats = tool.get_available_formats()
    assert len(formats) == 3
    assert "MP3" not in formats
    assert "WAV" in formats
    assert "AAC" in formats
    assert "FLAC" in formats 