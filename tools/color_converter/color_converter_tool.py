# tools/color_converter/color_converter_tool.py
from tool_interface import MiniTool


class ColorConverterTool(MiniTool):
    name = "Farbkonvertierer"
    def __init__(self):
        super().__init__(self.name, "ColorConverterTool")
        self.input_params = {}

    def execute_tool(self, input_params: dict) -> bool:
        # Automatische Weiterleitung zur separaten Route
        self.output = """
        <script>
            window.location.href = "/color_converter";
        </script>
        <div class="alert alert-info">
            <p>Sie werden zum Farbkonverter weitergeleitet...</p>
            <p>Wenn die Weiterleitung nicht funktioniert, <a href="/color_converter" class="btn btn-primary">klicken Sie hier</a>.</p>
        </div>
        """
        return True