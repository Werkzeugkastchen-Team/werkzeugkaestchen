from tool_interface import MiniTool


class JsonValidatorTool(MiniTool):
    name = "JsonValidator"
    description = "test."

    def __init__(self):
        super().__init__("JSON Validation Tool", "JsonValidatorTool")
        self.input_params = {
            "json_string": "string"
        }
    
    def execute_tool(self, input_params: dict) -> bool:
        import json
        try:
            json_string = input_params.get("json_string", "")
            json.loads(json_string)
            self.output = "Valid JSON"
            return True
        except json.JSONDecodeError as e:
            self.output = "Invalid JSON"
            self.error_message = str(e)
            return True
        except Exception as e:
            self.error_message = str(e)
            return False
