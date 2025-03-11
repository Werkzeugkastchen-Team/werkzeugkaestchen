from tool_interface import MiniTool, OutputType

class WordCounterTool(MiniTool):
    name = "Wortzähler"
    description = "Zählt die Anzahl der Wörter in einem Text, unter Berücksichtigung von Bindestrichen und Zeilenumbrüchen."
    
    def __init__(self):
        super().__init__(self.name, "WordCounterTool")
        self.input_params = {
            "text": "string",
            "count_hyphens": "boolean"
        }
    
    def execute_tool(self, input_params: dict) -> bool:
        try:
            text = input_params.get("text", "").strip()
            count_hyphens = input_params.get("count_hyphens", False)
            
            if not text:
                self.error_message = "Bitte geben Sie einen Text ein."
                return False
            
            # Replace multiple spaces and newlines with single space
            text = ' '.join(text.split())
            
            if count_hyphens:
                # Count hyphenated words as one word
                word_count = len(text.split())
            else:
                # Count hyphenated parts as separate words
                text = text.replace("-", " ")
                word_count = len(text.split())
            
            self.output = f"""
            <div class='card'>
                <div class='card-body'>
                    <h5>Ergebnis der Wortzählung:</h5>
                    <p>Anzahl der Wörter: <strong>{word_count}</strong></p>
                    <p><small>Hinweis: {'Bindestriche wurden als Wortverbindungen gezählt' if count_hyphens else 'Bindestriche wurden als Worttrenner gezählt'}.</small></p>
                </div>
            </div>
            """
            return True
            
        except Exception as e:
            self.error_message = f"Fehler bei der Verarbeitung: {str(e)}"
            return False 