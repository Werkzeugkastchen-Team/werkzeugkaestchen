import json
import html
from typing import Dict, Any
from tool_interface import MiniTool

class JSONFormatierungTool(MiniTool):
    def __init__(self):
        super().__init__("JSON-Formatierung", "JSONFormatierungTool")
        self.input_params = {
            "JSON Text": {
                "type": "textarea"
            }
        }
        self.formatted_json = ""
        self.description = "Formatiert JSON in ein lesbares Foramt (Pretty Print)"
        
    def execute_tool(self, input_params: Dict[str, Any]) -> bool:
        try:
            json_input = input_params.get("JSON Text", "").strip()
            
            if not json_input:
                self.error_message = "Bitte geben Sie JSON ein."
                return False
                
            parsed = json.loads(json_input)
            self.formatted_json = json.dumps(parsed, indent=4, ensure_ascii=False)
            self.output = self._create_formatted_output()
            return True
            
        except json.JSONDecodeError as e:
            self.output = self._create_error_output(e)
            return True
        except Exception as e:
            self.error_message = f"Fehler: {str(e)}"
            return False
    
    def _create_formatted_output(self) -> str:
        escaped_json = html.escape(self.formatted_json)
        return f"""
        <div class="json-formatter-result">
            <pre class="formatted-json">{escaped_json}</pre>
            <button onclick="copyToClipboard()" class="btn btn-success mt-3">
                In Zwischenablage kopieren
            </button>
        </div>
        <script>
            function copyToClipboard() {{
                const text = `{self.formatted_json}`;
                navigator.clipboard.writeText(text).then(() => {{
                    alert("Erfolgreich kopiert!");
                }});
            }}
        </script>
        """
    
    def _create_error_output(self, error: json.JSONDecodeError) -> str:
        return f"""
        <div class="alert alert-danger">
            <strong>✘ Ungültiges JSON:</strong> {error.msg}<br>
            <em>Position:</em> Zeile {error.lineno}, Spalte {error.colno}
        </div>
        """