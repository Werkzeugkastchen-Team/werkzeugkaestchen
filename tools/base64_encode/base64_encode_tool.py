import base64
from tool_interface import MiniTool

class Base64EncodeTool(MiniTool):
    def __init__(self):
        super().__init__("Base64 Encode Tool", "Base64EncodeTool")
        self.input_params = {
            "Text to encode": "string",
            "Encoding": {
                "type": "enum",
                "options": ["utf-8", "ascii"]
            }
        }
        self.description = "Encodes any input text to a Base64 String. Supports ascii and utf-8 encoding"
        
    def execute_tool(self, input_params: dict) -> bool:
        try:
            message = input_params.get("Text to encode", "")
            encoding = input_params.get("Encoding", "utf-8")
            
            if message == "":
                self.error_message = "Input text is empty or invalid"
                return False
                
            message_bytes = message.encode(encoding)
            base64_bytes = base64.b64encode(message_bytes)
            # utf-8 is needed for web-compatible display,
            # and it's backwards compatible with
            # ascii anyway
            base64_message = base64_bytes.decode('utf-8')
            
            self.output = base64_message
            return True
            
        except Exception as e:
            print(str(e))
            self.error_message = str(e)
            return False