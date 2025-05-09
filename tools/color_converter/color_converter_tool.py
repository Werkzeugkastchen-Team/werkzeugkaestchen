from tool_interface import MiniTool
from flask_babel import lazy_gettext as _


class ColorConverterTool(MiniTool):
    def __init__(self):
        super().__init__(_("Farbkonvertierer"), "ColorConverterTool")
        self.description = _("Konvertiert Farben zwischen verschiedenen Formaten (HEX, RGB, HSL) und zeigt eine Vorschau zur Visualisierung.")
        self.input_params = {}

    def execute_tool(self, input_params: dict) -> bool:
        # Texte für Übersetzung auslagern
        redirect_text = _("Sie werden zum Farbkonverter weitergeleitet...")
        fallback_text = _("Wenn die Weiterleitung nicht funktioniert,")
        click_here = _("klicken Sie hier")

        # Automatische Weiterleitung zur separaten Route
        self.output = f"""
        <script>
            window.location.href = "/color_converter";
        </script>
        <div class="alert alert-info">
            <p>{redirect_text}</p>
            <p>{fallback_text} <a href="/color_converter" class="btn btn-primary">{click_here}</a>.</p>
        </div>
        """
        return True