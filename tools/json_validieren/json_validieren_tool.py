import json
from typing import Dict, Any
from tool_interface import MiniTool

class JSONValidierungTool(MiniTool):
    def __init__(self):
        super().__init__("JSON-Validierung", "JSONValidierungTool")
        self.input_params = {
            "json_text": {
                "type": "string",
                "label": "JSON-Text",
                "placeholder": "Fügen Sie Ihren JSON-Text hier ein"
            }
        }
        self.is_valid = False
        self.error_details = {}

    def execute_tool(self, input_params: Dict[str, Any]) -> bool:
        try:
            json_text = input_params.get("json_text", "").strip()
            
            if not json_text:
                self.error_message = "Bitte geben Sie JSON-Text ein."
                return False

            # Validierung durchführen
            json.loads(json_text)
            self.is_valid = True
            self.output = self._create_success_output()
            return True

        except json.JSONDecodeError as e:
            self.error_details = {
                "message": f"Ungültiges JSON: {e.msg}",
                "line": e.lineno,
                "column": e.colno,
                "position": e.pos
            }
            self.output = self._create_error_output()
            return True  # Fehler wird als Output behandelt, kein Tool-Fehler
        except Exception as e:
            self.error_message = f"Unerwarteter Fehler: {str(e)}"
            return False

    def _create_success_output(self) -> str:
        return """
        <div class="alert alert-success">
            <strong>✓ Gültiges JSON!</strong> Die Syntax ist korrekt.
        </div>
        """

    def _create_error_output(self) -> str:
        return f"""
        <div class="alert alert-danger">
            <strong>✘ Fehler:</strong> {self.error_details['message']}<br>
            <em>Position:</em> Zeile {self.error_details['line']}, Spalte {self.error_details['column']}
        </div>
        """