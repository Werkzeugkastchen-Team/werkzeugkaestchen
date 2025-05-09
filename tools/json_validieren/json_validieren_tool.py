import json
from typing import Dict, Any
from tool_interface import MiniTool
from flask_babel import lazy_gettext as _


class JSONValidierungTool(MiniTool):
    def __init__(self):
        super().__init__(_("JSON-Validierung"), "JSONValidierungTool")
        self.input_params = {
            _("JSON Text"): {
                "type": "textarea"
            }
        }
        self.is_valid = False
        self.error_details = {}
        self.description = _("Validiert JSON und schaut, ob der Text syntaktisch korrektes JSON ist.")

    def execute_tool(self, input_params: Dict[str, Any]) -> bool:
        try:
            json_text = input_params.get(_("JSON Text"), "").strip()

            if not json_text:
                self.error_message = _("Bitte geben Sie JSON-Text ein.")
                return False

            # Validierung durchführen
            json.loads(json_text)
            self.is_valid = True
            self.output = self._create_success_output()
            return True

        except json.JSONDecodeError as e:
            error_msg = _("Ungültiges JSON:")
            self.error_details = {
                "message": f"{error_msg} {e.msg}",
                "line": e.lineno,
                "column": e.colno,
                "position": e.pos
            }
            self.output = self._create_error_output()
            return True  # Fehler wird als Output behandelt, kein Tool-Fehler
        except Exception as e:
            error_msg = _("Unerwarteter Fehler:")
            self.error_message = f"{error_msg} {str(e)}"
            return False

    def _create_success_output(self) -> str:
        # Extrahiere alle zu übersetzenden Strings vorab
        valid_json_text = _("Gültiges JSON!")
        syntax_correct_text = _("Die Syntax ist korrekt.")

        return f"""
        <div class="alert alert-success">
            <strong>✓ {valid_json_text}</strong> {syntax_correct_text}
        </div>
        """

    def _create_error_output(self) -> str:
        # Extrahiere alle zu übersetzenden Strings vorab
        error_text = _("Fehler:")
        position_text = _("Position:")
        line_text = _("Zeile")
        column_text = _("Spalte")

        return f"""
        <div class="alert alert-danger">
            <strong>✘ {error_text}</strong> {self.error_details['message']}<br>
            <em>{position_text}</em> {line_text} {self.error_details['line']}, {column_text} {self.error_details['column']}
        </div>
        """