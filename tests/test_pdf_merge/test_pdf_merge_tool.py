import os
import tempfile
import pytest
from unittest.mock import MagicMock, patch, mock_open
from tools.pdf_merge.pdf_merge_tool import PdfMergeTool


@pytest.fixture
def pdf_merge_tool():
    return PdfMergeTool()


def test_init(pdf_merge_tool):
    assert pdf_merge_tool.name == "PDF Merge Tool"
    assert pdf_merge_tool.identifier == "PdfMergeTool"
    assert "pdf_files" in pdf_merge_tool.input_params


def test_execute_less_than_two_files(pdf_merge_tool):
    # No files
    result = pdf_merge_tool.execute_tool({})
    assert not result
    assert "mindestens zwei" in pdf_merge_tool.error_message

    # Only one file
    result = pdf_merge_tool.execute_tool({
        "pdf_files": [{
            "file_path": "one.pdf",
            "filename": "one.pdf"
        }],
        "pdf_order": "one.pdf"
    })
    assert not result
    assert "mindestens zwei" in pdf_merge_tool.error_message


def test_execute_missing_order(pdf_merge_tool):
    result = pdf_merge_tool.execute_tool({
        "pdf_files": [
            {"file_path": "a.pdf", "filename": "a.pdf"},
            {"file_path": "b.pdf", "filename": "b.pdf"}
        ]
    })
    assert not result
    assert "Keine Reihenfolge" in pdf_merge_tool.error_message


def test_execute_invalid_order(pdf_merge_tool):
    result = pdf_merge_tool.execute_tool({
        "pdf_files": [
            {"file_path": "a.pdf", "filename": "a.pdf"},
            {"file_path": "b.pdf", "filename": "b.pdf"}
        ],
        "pdf_order": "c.pdf,b.pdf"
    })
    assert not result
    assert "nicht gefunden" in pdf_merge_tool.error_message


@patch('tools.pdf_merge.pdf_merge_tool.PdfMerger')
@patch('tools.pdf_merge.pdf_merge_tool.base64.b64encode')
@patch('builtins.open', new_callable=mock_open)
def test_execute_success(mock_open_file, mock_b64encode, mock_merger_class, pdf_merge_tool):
    mock_merger = MagicMock()
    mock_merger_class.return_value = mock_merger
    mock_b64encode.return_value = b"base64dummy"

    input_files = [
        {"file_path": "fileA.pdf", "filename": "fileA.pdf"},
        {"file_path": "fileB.pdf", "filename": "fileB.pdf"}
    ]

    result = pdf_merge_tool.execute_tool({
        "pdf_files": input_files,
        "pdf_order": "fileB.pdf,fileA.pdf"
    })

    assert result
    assert mock_merger.append.call_count == 2
    assert mock_merger.write.call_count == 1
    assert "erfolgreich zusammengeführt" in pdf_merge_tool.output


def test_get_file_base64(pdf_merge_tool):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"Hello Test PDF")
        tmp_path = tmp.name

    try:
        result = pdf_merge_tool._get_file_base64(tmp_path)
        assert isinstance(result, str)
        assert "SGVsbG8gVGVzdCBQREY=" in result  # base64 of "Hello Test PDF"
    finally:
        os.remove(tmp_path)
