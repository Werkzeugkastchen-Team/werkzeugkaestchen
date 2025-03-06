import os
import tempfile
import qrcode
from tool_interface import MiniTool


class QrCodeGeneratorTool(MiniTool):
    def __init__(self):
        super().__init__("QR-Code Generator", "QrCodeGeneratorTool")
        self.description = "Erstellt QR-Codes aus Text oder URLs"
        self.input_params = {
            "text": "string",
            "error_correction": "string",
            "box_size": "string",
            "border": "string"
        }

    def execute_tool(self, input_params: dict) -> bool:
        try:
            # Get parameters
            text = input_params.get("text", "")
            if not text:
                self.error_message = "Bitte geben Sie einen Text oder eine URL ein"
                return False

            # QR code settings with defaults
            error_correction_text = input_params.get("error_correction", "M")
            box_size = int(input_params.get("box_size", "10"))
            border = int(input_params.get("border", "4"))

            # Map error correction level string to qrcode constants
            error_correction_map = {
                "L": qrcode.constants.ERROR_CORRECT_L,  # 7% recovery
                "M": qrcode.constants.ERROR_CORRECT_M,  # 15% recovery
                "Q": qrcode.constants.ERROR_CORRECT_Q,  # 25% recovery
                "H": qrcode.constants.ERROR_CORRECT_H   # 30% recovery
            }
            error_correction = error_correction_map.get(
                error_correction_text, qrcode.constants.ERROR_CORRECT_M)

            # Create QR code instance
            qr = qrcode.QRCode(
                version=1,
                error_correction=error_correction,
                box_size=box_size,
                border=border,
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

            # Create HTML output with QR code and text details
            result = f"""
            <div class="qr-code-result">
                <div class="row">
                    <div class="col-md-6">
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
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header bg-info text-white">
                                <h5 class="mb-0">QR-Code Details</h5>
                            </div>
                            <div class="card-body">
                                <table class="table">
                                    <tbody>
                                        <tr>
                                            <th>Inhalt:</th>
                                            <td>{text}</td>
                                        </tr>
                                        <tr>
                                            <th>Fehlerkorrektur:</th>
                                            <td>{error_correction_text} ({self._get_error_correction_description(error_correction_text)})</td>
                                        </tr>
                                        <tr>
                                            <th>Box-Größe:</th>
                                            <td>{box_size} Pixel</td>
                                        </tr>
                                        <tr>
                                            <th>Rand:</th>
                                            <td>{border} Einheiten</td>
                                        </tr>
                                    </tbody>
                                </table>
                                <div class="alert alert-info mt-3">
                                    <strong>Tipp:</strong> Scannen Sie den QR-Code mit der Kamera-App 
                                    Ihres Smartphones oder einem QR-Code-Scanner.
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

    def _get_error_correction_description(self, level):
        """Return description for error correction level"""
        descriptions = {
            "L": "Niedrig - 7% Fehlerkorrektur",
            "M": "Mittel - 15% Fehlerkorrektur",
            "Q": "Quartil - 25% Fehlerkorrektur",
            "H": "Hoch - 30% Fehlerkorrektur"
        }
        return descriptions.get(level, "Unbekannt")
