import base64
from tool_interface import MiniTool

class Base64EncodeTool(MiniTool):
    def __init__(self):
        super().__init__("Base64 Kodierungstool", "Base64EncodeTool")
        self.input_params = {
            "Zu kodierender Text": "string",
            "Kodierung": {
                "type": "enum",
                "options": ["utf-8", "ascii"]
            }
        }
        self.description = "Kodiert jeden Eingabetext in einen Base64-String. Unterstützt ASCII- und UTF-8-Kodierung"

    def execute_tool(self, input_params: dict) -> bool:
        try:
            message = input_params.get("Zu kodierender Text", "")
            encoding = input_params.get("Kodierung", "utf-8")

            if message == "":
                self.error_message = "Eingabetext ist leer oder ungültig"
                return False

            message_bytes = message.encode(encoding)
            base64_bytes = base64.b64encode(message_bytes)
            # utf-8 ist nötig für webkompatible Darstellung
            # und ist ohnehin abwärtskompatibel mit
            # ascii
            base64_message = base64_bytes.decode('utf-8')

            self.output = base64_message
            return True

        except Exception as e:
            print(str(e))
            self.error_message = str(e)
            return False