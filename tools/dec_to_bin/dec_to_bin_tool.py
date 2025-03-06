from tool_interface import MiniTool

class DecToBinTool(MiniTool):
    name = "JsonValidator"
    description = "test."
    
    def __init__(self):
        super().__init__("Decimal to Binary Tool", "DecToBinTool")
        self.input_params = {
            "text" : "string"
        }
        
    def execute_tool(self, input_params: dict) -> bool:
        try:
            text = input_params.get("text", "")
            num = int(text)
            converted = bin(num)
            # remove 0b
            output_str = converted[2:]
            self.output = output_str
            return True
        except Exception as e:
            print(str(e))
            self.error_message = str(e)
            return False