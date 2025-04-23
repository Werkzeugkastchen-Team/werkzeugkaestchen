import base64
from flask_babel import lazy_gettext as _
from tool_interface import MiniTool

class Base64EncodeTool(MiniTool):
    def __init__(self):
        # Der übergebene Name wird im Interface angezeigt und ist somit übersetzbar.
        super().__init__(_("Base64 Kodierungstool"), "Base64EncodeTool")
        # Beachte: Die Keys in input_params werden hier für die UI genutzt.
        # Wenn du diese Keys übersetzen möchtest, werden auch die entsprechenden Eingabewerte
        # unter den übersetzten Keys erwartet.
        self.input_params = {
            _("Zu kodierender Text"): "string",
            _("Kodierung"): {
                "type": "enum",
                "options": ["utf-8", "ascii"]
            }
        }
        self.description = _("base64_encode_tool_description")

    def execute_tool(self, input_params: dict) -> bool:
        try:
            # Definiere die Schlüssel, wie sie auch in input_params verwendet wurden
            text_key = _("Zu kodierender Text")
            encoding_key = _("Kodierung")
            message = input_params.get(text_key, "")
            encoding = input_params.get(encoding_key, "utf-8")

            if message == "":
                self.error_message = _("Eingabetext ist leer oder ungültig")
                return False

            message_bytes = message.encode(encoding)
            base64_bytes = base64.b64encode(message_bytes)
            # UTF-8-Encoding sorgt für eine webkompatible Darstellung
            base64_message = base64_bytes.decode('utf-8')

            self.output = base64_message
            return True

        except Exception as e:
            print(str(e))
            self.error_message = str(e)
            return False
