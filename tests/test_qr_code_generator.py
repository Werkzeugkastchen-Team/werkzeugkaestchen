import os
import base64
import tempfile
import pytest
from unittest.mock import patch, MagicMock
from tools.qr_code_generator.qr_code_generator_tool import QrCodeGeneratorTool


class TestQrCodeGeneratorTool:
    def setup_method(self):
        """Setup a fresh instance of the tool before each test."""
        self.tool = QrCodeGeneratorTool()

    def test_init(self):
        """Test that the tool is initialized with correct attributes."""
        assert self.tool.name == "QR-Code Generator"
        assert self.tool.identifier == "QrCodeGeneratorTool"
        assert "Erstellt QR-Codes" in self.tool.description
        assert "text" in self.tool.input_params
        assert self.tool.input_params["text"] == "string"

    def test_empty_input(self):
        """Test that the tool handles empty input correctly."""
        # Test with empty text
        result = self.tool.execute_tool({"text": ""})
        assert result is False
        assert "Bitte geben Sie einen Text oder eine URL ein" in self.tool.error_message

        # Test with no text parameter
        result = self.tool.execute_tool({})
        assert result is False
        assert "Bitte geben Sie einen Text oder eine URL ein" in self.tool.error_message

    @patch('qrcode.QRCode')
    def test_qr_code_creation(self, mock_qrcode):
        """Test that QR code is created with correct parameters."""
        # Setup mock QR code
        mock_qr_instance = MagicMock()
        mock_qrcode.return_value = mock_qr_instance

        # Mock the image creation
        mock_image = MagicMock()
        mock_qr_instance.make_image.return_value = mock_image

        # Mock the get_image_base64 method to return a test string
        with patch.object(self.tool, '_get_image_base64', return_value='test_base64_string'):
            # Execute the tool
            result = self.tool.execute_tool({"text": "https://example.com"})

            # Check the result
            assert result is True

            # Verify QRCode was created with correct parameters
            mock_qrcode.assert_called_once_with(
                version=1,
                # ERROR_CORRECT_M is usually 1
                error_correction=pytest.approx(1),
                box_size=10,
                border=4
            )

            # Verify data was added and QR code was generated
            mock_qr_instance.add_data.assert_called_once_with(
                "https://example.com")
            mock_qr_instance.make.assert_called_once_with(fit=True)
            mock_qr_instance.make_image.assert_called_once_with(
                fill_color="black", back_color="white")

            # Verify image was saved
            mock_image.save.assert_called_once()

            # Verify output contains the expected elements
            assert "qr-code-result" in self.tool.output
            assert "test_base64_string" in self.tool.output
            assert "QR-Code herunterladen" in self.tool.output

    def test_get_image_base64(self):
        """Test the _get_image_base64 method with a real image."""
        # Create a small test image file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        temp_file.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')
        temp_file.close()

        try:
            # Get base64 string
            base64_string = self.tool._get_image_base64(temp_file.name)

            # Verify it's a valid base64 string
            assert isinstance(base64_string, str)
            # Try to decode it to ensure it's valid base64
            decoded = base64.b64decode(base64_string)
            assert isinstance(decoded, bytes)

        finally:
            # Clean up test file
            os.unlink(temp_file.name)

    def test_exception_handling(self):
        """Test that exceptions are handled correctly."""
        # Patch make_image to raise an exception
        with patch('qrcode.QRCode.make_image', side_effect=Exception("Test error")):
            result = self.tool.execute_tool({"text": "test"})

            # Check the result
            assert result is False
            assert "Fehler bei der QR-Code Erstellung" in self.tool.error_message
            assert "Test error" in self.tool.error_message
