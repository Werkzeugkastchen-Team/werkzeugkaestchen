from tool_interface import MiniTool
from pydantic import ConfigDict
from flask_babel import lazy_gettext as _

import platform

def get_api_base_url():
    """Get API base URL based on platform. Some combinations require different base URLs."""
    host = "127.0.0.1"
    sys = platform.system().lower()
    if sys.startswith("win"):
        host = "host.docker.internal"
    return f"http://{host}:11434"

METAPROMPT_EN = """
Summarize the following text. The Summary must be in English. Be short, concise and truthful. Immediately respond with the contents of your summary:
"""

METAPROMPT_DE = """
Fasse den folgenden Text zusammen. Die Zusammenfassung muss auf Deutsch sein. Halte dich kurz und wahrheitsgetrau. Antworte sofort mit dem Inhalt der Zusammenfassung:
"""

MAX_CHARS = 8_000


class TextSummaryTool(MiniTool):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self):
        super().__init__(_("Text zusammenfassen Tool"), "TextSummaryTool")
        self.input_params = {
            _("Text"): "string",
            _("Sprache"): {
                "type": "enum",
                "options": ["de", "en"]
            },
            _("Model"): {
                "type": "enum",
                "options": ["gemma3:4b-it-qat", "gemma3:1b"]
            }
        }
        self.description = _("Fasst Texte mithilfe von Sprachmodellen (LLMs) zusammen.")
        
    def execute_tool(self, input_params: dict) -> bool:
        try:
            from litellm import completion
            
            self.error_message = ""
            
            text_to_summarize = input_params.get(_("Text"), "")
            if not text_to_summarize:
                self.error_message = _("Der Eingabetext ist leer oder ungültig.")
                return False
            
            if len(text_to_summarize) > MAX_CHARS:
                self.error_message = _("Der Eingabetext is zu lang.")
                return False
            
            language = input_params.get(_("Sprache"), "de")
            model = input_params.get(_("Model"), "gemma3:4b-it-qat")
            
            meta_prompt = METAPROMPT_DE if language == "de" else METAPROMPT_EN

            prompt = meta_prompt + " \n " + text_to_summarize
            
            print("trying to connect to ollama backend with url " + get_api_base_url())
            
            response = completion(
                model=f"ollama/{model}",
                messages=[{ "content": prompt,"role": "user"}],
                api_base=get_api_base_url()
            )

            summary = response.choices[0].message.content
            self.output = summary
            return True
        except Exception as e:
            print(str(e))
            self.error_message = str(e)
            return False
