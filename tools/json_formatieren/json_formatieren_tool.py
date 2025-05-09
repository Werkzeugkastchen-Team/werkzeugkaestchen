import json
import html
from typing import Dict, Any
from tool_interface import MiniTool
from flask_babel import lazy_gettext as _


class JSONFormatierungTool(MiniTool):
    def __init__(self):
        super().__init__(_("JSON-Formatierung"), "JSONFormatierungTool")
        self.input_params = {
            _("JSON Text"): {
                "type": "textarea"
            }
        }
        self.formatted_json = ""
        self.description = _("Formatiert JSON in ein lesbares Format (Pretty Print)")

    def execute_tool(self, input_params: Dict[str, Any]) -> bool:
        try:
            json_input = input_params.get(_("JSON Text"), "").strip()

            if not json_input:
                self.error_message = _("Bitte geben Sie JSON ein.")
                return False

            parsed = json.loads(json_input)
            self.formatted_json = json.dumps(parsed, indent=4, ensure_ascii=False)
            self.output = self._create_formatted_output()
            return True

        except json.JSONDecodeError as e:
            self.output = self._create_error_output(e)
            return True
        except Exception as e:
            error_msg = _("Fehler:")
            self.error_message = f"{error_msg} {str(e)}"
            return False

    def _create_formatted_output(self) -> str:
        # Text für Babel extrahieren
        copy_btn_text = _("In Zwischenablage kopieren")
        copy_success_msg = _("Erfolgreich kopiert!")

        escaped_json = html.escape(self.formatted_json)
        return f"""
        <div class="json-formatter-result">
            <pre class="formatted-json">{escaped_json}</pre>
            <button onclick="copyToClipboard()" class="btn btn-success mt-3">
                {copy_btn_text}
            </button>
        </div>
        <script>
            function copyToClipboard() {{
                const text = `{self.formatted_json}`;
                navigator.clipboard.writeText(text).then(() => {{
                    alert("{copy_success_msg}");
                }});
            }}
        </script>
        """

    def _create_error_output(self, error: json.JSONDecodeError) -> str:
        # Text für Babel extrahieren
        invalid_json_text = _("Ungültiges JSON:")
        position_text = _("Position:")
        line_text = _("Zeile")
        column_text = _("Spalte")

        return f"""
        <div class="alert alert-danger">
            <strong>✘ {invalid_json_text}</strong> {error.msg}<br>
            <em>{position_text}</em> {line_text} {error.lineno}, {column_text} {error.colno}
        </div>
        """