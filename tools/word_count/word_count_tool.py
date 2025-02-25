
from tool_interface import MiniTool


class WordCountTool(MiniTool):
    def __init__(self):
        super().__init__("Word Counting Tool", "WordCountTool")
        self.input_params = {
            "text": "string",
            "count_hyphens": "boolean"
        }
    
    def execute_tool(self, input_params: dict) -> bool:
        try:
            text = input_params.get("text", "")
            count_hyphens = input_params.get("count_hyphens", False)
            if count_hyphens:
                self.output = str(len(text.split()))
            else:
                self.output = str(len(text.replace("-", "").split()))
            return True
        except Exception as e:
            self.error_message = str(e)
            return False

