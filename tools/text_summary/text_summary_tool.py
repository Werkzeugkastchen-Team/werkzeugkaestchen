from tool_interface import MiniTool


METAPROMPT = """
Summarize the following text. The Summary must be in the same language as the source text. Be short, concise and truthful. Immediately respond with the contents of your summary:
"""

class TextSummaryTool(MiniTool):
    def __init__(self):
        super().__init__("Text zusammenfassen Tool", "TextSummaryTool")
        # TODO: parameter for model. Gemma3:1b and Gemma3:4b
        self.input_params = {
            "Text": "string"
        }
        self.description = "Fasst Texte mithilfe von Sprachmodellen (LLMs) zusammen."
        
    def execute_tool(self, input_params: dict) -> bool:
        try:
            from litellm import completion
            
            text_to_summarize = input_params.get("Text", "")
            if not text_to_summarize:
                self.error_message = "Input text is empty or invalid"
                return False

            prompt = METAPROMPT + " \n " + text_to_summarize

            # TODO: Make model configurable via input_params
            response = completion(
                model="ollama/gemma3:1b", 
                messages=[{ "content": prompt,"role": "user"}], 
                api_base="http://localhost:11434" # Assuming Ollama runs locally
            )
            
            summary = response.choices[0].message.content
            self.output = summary
            return True
        except Exception as e:
            print(str(e))
            self.error_message = str(e)
            return False
