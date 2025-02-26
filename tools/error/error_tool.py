from tool_interface import MiniTool

class ErrorTool(MiniTool):
    def __init__(self):
        super().__init__("Error Tool", "ErrorTool")
        self.input_params = {
            "json_string": "string"
        }
        
    def execute_tool(self, input_params: dict) -> bool:
        self.error_message = "Mein Fehler"
        return False