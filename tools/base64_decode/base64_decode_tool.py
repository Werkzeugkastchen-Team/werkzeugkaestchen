import base64
from tool_interface import MiniTool

class Base64DecodeTool(MiniTool):
    def __init__(self):
        super().__init__("Base64 Decode Tool", "Base64DecodeTool")
        self.input_params = {
            "Base64 String to decode": "string",
            "Encoding": {
                "type": "enum",
                "options": ["utf-8", "ascii"]
            }
        }
        self.description = "Decodes a Base64 String to text. Supports ascii and utf-8 encoding"
        
    def execute_tool(self, input_params: dict) -> bool:
        try:
            base64_message = input_params.get("Base64 String to decode", "")
            encoding = input_params.get("Encoding", "utf-8")
            
            if base64_message == "":
                self.error_message = "Base64 Input String is empty or invalid"
                return False
            
            decoded_bytes = base64.b64decode(base64_message)
            decoded_message = decoded_bytes.decode(encoding)
            
            self.output = decoded_message
            return True
        except Exception as e:
            print(str(e))
            self.error_message = str(e)
            return False