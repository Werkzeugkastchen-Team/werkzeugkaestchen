# python
import os
import tempfile
import qrcode
from flask_babel import lazy_gettext as _
from tool_interface import MiniTool

class QrCodeGeneratorTool(MiniTool):
    def __init__(self):
        super().__init__(_(r"QR\-Code Generator"), "QrCodeGeneratorTool")
        self.description = _(r"Erstellt QR\-Codes aus Text oder URLs")
        self.input_params = {
            _(r"Text oder URL"): "string"
        }

    def execute_tool(self, input_params: dict) -> bool:
        try:
            # Abfrage des Texteingabeparameters
            text = input_params.get(_(r"Text oder URL"), "")
            if not text:
                self.error_message = _(r"Bitte geben Sie einen Text oder eine URL ein")
                return False

            # Erzeugung des QR‑Codes mit Standard­einstellungen
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )

            qr.add_data(text)
            qr.make(fit=True)

            # Erzeugung eines Bildes
            img = qr.make_image(fill_color="black", back_color="white")

            # Speicherung des Bildes im temporären Verzeichnis
            temp_dir = tempfile.gettempdir()
            file_path = os.path.join(temp_dir, "qrcode.png")
            img.save(file_path)

            # Zusammenbau des HTML Ergebnisses mit Übersetzungen
            image_base64 = self._get_image_base64(file_path)
            result = (
                "<div class=\"qr-code-result\">"
                    "<div class=\"row\">"
                        "<div class=\"col-md-6 mx-auto\">"
                            "<div class=\"card\">"
                                "<div class=\"card-header bg-primary text-white\">"
                                    "<h5 class=\"mb-0\">" + _(r"Ihr QR\-Code") + "</h5>"
                                "</div>"
                                "<div class=\"card-body text-center\">"
                                    "<img src=\"data:image/png;base64," + image_base64 + 
                                    "\" alt=\"" + _(r"QR\-Code") + "\" class=\"img-fluid\">"
                                    "<div class=\"mt-3\">"
                                        "<a href=\"data:image/png;base64," + image_base64 + 
                                        "\" download=\"qrcode.png\" class=\"fancy-button\">" + _(r"QR\-Code herunterladen") + "</a>"
                                    "</div>"
                                "</div>"
                            "</div>"
                        "</div>"
                    "</div>"
                "</div>"
            )

            self.output = result
            return True

        except Exception as e:
            self.error_message = _(r"Fehler bei der QR\-Code Erstellung:") + " " + str(e)
            return False

    def _get_image_base64(self, image_path):
        """Convert image to base64 string for embedding in HTML"""
        import base64
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")