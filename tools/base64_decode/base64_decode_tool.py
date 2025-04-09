import base64
from tool_interface import MiniTool

class Base64DecodeTool(MiniTool):
    def __init__(self):
        super().__init__("Base64 Dekodierungstool", "Base64DecodeTool")
        self.input_params = {
            "Zu dekodierender Base64-String": "string",
            "Kodierung": {
                "type": "enum",
                "options": ["utf-8", "ascii"]
            }
        }
        self.description = "Dekodiert einen Base64-String zu Text. Unterstützt ASCII- und UTF-8-Kodierung"

    def execute_tool(self, input_params: dict) -> bool:
        try:
            base64_message = input_params.get("Zu dekodierender Base64-String", "")
            encoding = input_params.get("Kodierung", "utf-8")

            if base64_message == "":
                self.error_message = "Base64-Eingabestring ist leer oder ungültig"
                return False

            decoded_bytes = base64.b64decode(base64_message)
            decoded_message = decoded_bytes.decode(encoding)

            self.output = decoded_message
            return True
        except Exception as e:
            print(str(e))
            self.error_message = str(e)
            return False