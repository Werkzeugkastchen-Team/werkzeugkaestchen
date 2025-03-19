import os
import tempfile
import qrcode
from tool_interface import MiniTool


class QrCodeGeneratorTool(MiniTool):
    def __init__(self):
        super().__init__("QR-Code Generator", "QrCodeGeneratorTool")
        self.description = "Erstellt QR-Codes aus Text oder URLs"
        self.input_params = {
            "text": "string"
        }

    def execute_tool(self, input_params: dict) -> bool:
        try:
            # Get text parameter
            text = input_params.get("text", "")
            if not text:
                self.error_message = "Bitte geben Sie einen Text oder eine URL ein"
                return False

            # Create QR code with default settings
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,  # Medium error correction
                box_size=10,
                border=4,
            )

            # Add data to QR code
            qr.add_data(text)
            qr.make(fit=True)

            # Create an image from the QR Code
            img = qr.make_image(fill_color="black", back_color="white")

            # Save the image to a temporary file
            temp_dir = tempfile.gettempdir()
            file_path = os.path.join(temp_dir, "qrcode.png")
            img.save(file_path)

            # Create simplified HTML output with QR code
            result = f"""
            <div class="qr-code-result">
                <div class="row">
                    <div class="col-md-6 mx-auto">
                        <div class="card">
                            <div class="card-header bg-primary text-white">
                                <h5 class="mb-0">Ihr QR-Code</h5>
                            </div>
                            <div class="card-body text-center">
                                <img src="data:image/png;base64,{self._get_image_base64(file_path)}" 
                                     alt="QR Code" class="img-fluid">
                                <div class="mt-3">
                                    <a href="data:image/png;base64,{self._get_image_base64(file_path)}" 
                                       download="qrcode.png" class="fancy-button">
                                       QR-Code herunterladen
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """

            self.output = result
            return True

        except Exception as e:
            self.error_message = f"Fehler bei der QR-Code Erstellung: {str(e)}"
            return False

    def _get_image_base64(self, image_path):
        """Convert image to base64 string for embedding in HTML"""
        import base64
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
