from tool_interface import MiniTool
from pydantic import ConfigDict


METAPROMPT_EN = """
Summarize the following text. The Summary must be in English. Be short, concise and truthful. Immediately respond with the contents of your summary:
"""

METAPROMPT_DE = """
Fasse den folgenden Text zusammen. Die Zusammenfassung muss auf Deutsch sein. Halte dich kurz und wahrheitsgetrau. Antworte sofort mit dem Inhalt der Zusammenfassung:
"""

class TextSummaryTool(MiniTool):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self):
        super().__init__("Text zusammenfassen Tool", "TextSummaryTool")
        # TODO: parameter for model. Gemma3:1b and Gemma3:4b
        self.input_params = {
            "Text": "string",
            "Sprache": {
                "type": "enum",
                "options": ["de", "en"]
            },
            "Model": {
                "type": "enum",
                "options": ["gemma3:4b", "gemma3:1b"]
            }
        }
        self.description = "Fasst Texte mithilfe von Sprachmodellen (LLMs) zusammen."
        
    def execute_tool(self, input_params: dict) -> bool:
        try:
            from litellm import completion
            
            text_to_summarize = input_params.get("Text", "")
            if not text_to_summarize:
                self.error_message = "Input text is empty or invalid"
                return False
            
            language = input_params.get("Sprache", "de")
            model = input_params.get("Model", "gemma3:4b")
            
            meta_prompt = METAPROMPT_DE if language == "de" else METAPROMPT_EN
            

            prompt = meta_prompt + " \n " + text_to_summarize

            # TODO: Make model configurable via input_params
            response = completion(
                model=f"ollama/{model}", 
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
