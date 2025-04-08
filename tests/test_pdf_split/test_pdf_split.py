import os
import pytest
import tempfile
from unittest.mock import MagicMock, patch, mock_open
from PyPDF2 import PdfWriter
from tools.pdf_split.pdf_split_tool import PdfSplitTool


@pytest.fixture
def pdf_split_tool():
    return PdfSplitTool()


def create_mock_pdf(pages=10):
    """Create a mock PDF with the specified number of pages"""
    # Create a mock PDF reader
    mock_pdf = MagicMock()
    mock_pdf.pages = [MagicMock() for _ in range(pages)]
    return mock_pdf


def test_init(pdf_split_tool):
    """Test initialization of tool"""
    assert pdf_split_tool.name == "PDF Split Tool"
    assert pdf_split_tool.identifier == "PdfSplitTool"
    assert "pdf_file" in pdf_split_tool.input_params
    assert "split_page" in pdf_split_tool.input_params


def test_execute_no_file(pdf_split_tool):
    """Test error when no file is provided"""
    result = pdf_split_tool.execute_tool({"split_page": "3"})
    assert not result
    assert "wählen Sie eine PDF-Datei" in pdf_split_tool.error_message


def test_execute_no_split_page(pdf_split_tool):
    """Test error when no split page is provided"""
    result = pdf_split_tool.execute_tool({
        "pdf_file": {
            "file_path": "test.pdf",
            "filename": "test.pdf"
        }
    })
    assert not result
    assert "geben Sie eine Seitenzahl" in pdf_split_tool.error_message


def test_execute_invalid_split_page(pdf_split_tool):
    """Test error when invalid split page is provided"""
    result = pdf_split_tool.execute_tool({
        "pdf_file": {
            "file_path": "test.pdf",
            "filename": "test.pdf"
        },
        "split_page": "abc"
    })
    assert not result
    assert "gültige Seitenzahl" in pdf_split_tool.error_message


def test_execute_split_page_too_small(pdf_split_tool):
    """Test error when split page is too small"""
    result = pdf_split_tool.execute_tool({
        "pdf_file": {
            "file_path": "test.pdf",
            "filename": "test.pdf"
        },
        "split_page": "1"
    })
    assert not result
    assert "mindestens 2" in pdf_split_tool.error_message


@patch('tools.pdf_split.pdf_split_tool.PdfReader')
@patch('tools.pdf_split.pdf_split_tool.PdfWriter')
@patch('builtins.open', new_callable=mock_open)
def test_execute_split_page_too_large(mock_open_file, mock_writer_class, mock_reader_class, pdf_split_tool):
    """Test error when split page is larger than the total number of pages"""
    # Setup mock
    mock_reader = create_mock_pdf(5)  # Create a 5-page PDF
    mock_reader_class.return_value = mock_reader
    
    # Execute
    result = pdf_split_tool.execute_tool({
        "pdf_file": {
            "file_path": "test.pdf",
            "filename": "test.pdf"
        },
        "split_page": "10"
    })
    
    # Assert
    assert not result
    assert "kleiner sein als die Gesamtseitenzahl" in pdf_split_tool.error_message


@patch('tools.pdf_split.pdf_split_tool.PdfReader')
@patch('tools.pdf_split.pdf_split_tool.PdfWriter')
@patch('tools.pdf_split.pdf_split_tool.base64.b64encode')
@patch('builtins.open', new_callable=mock_open)
def test_execute_success(mock_open_file, mock_b64encode, mock_writer_class, mock_reader_class, pdf_split_tool):
    """Test successful PDF splitting"""
    # Setup mocks
    mock_reader = create_mock_pdf(10)  # Create a 10-page PDF
    mock_reader_class.return_value = mock_reader
    
    mock_part1_writer = MagicMock()
    mock_part2_writer = MagicMock()
    mock_writer_class.side_effect = [mock_part1_writer, mock_part2_writer]
    
    mock_b64encode.return_value = b"dummy_base64"
    
    # Execute
    result = pdf_split_tool.execute_tool({
        "pdf_file": {
            "file_path": "test.pdf",
            "filename": "test.pdf"
        },
        "split_page": "4"
    })
    
    # Assert
    assert result
    assert mock_part1_writer.add_page.call_count == 3  # Pages 0,1,2
    assert mock_part2_writer.add_page.call_count == 7  # Pages 3,4,5,6,7,8,9
    assert mock_part1_writer.write.call_count == 1
    assert mock_part2_writer.write.call_count == 1
    assert "erfolgreich geteilt" in pdf_split_tool.output


def test_get_file_base64(pdf_split_tool):
    """Test base64 conversion of a file"""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b"Test content")
        temp_path = temp_file.name
    
    try:
        # Test the function
        base64_content = pdf_split_tool._get_file_base64(temp_path)
        assert base64_content == "VGVzdCBjb250ZW50"  # Base64 for "Test content"
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)