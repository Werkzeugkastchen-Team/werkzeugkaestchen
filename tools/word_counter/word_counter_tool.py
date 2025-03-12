from tool_interface import MiniTool

class WordCounterTool(MiniTool):
    name = "Wortzähler"
    description = "Zählt die Anzahl der Wörter in einem Text, unter Berücksichtigung von Bindestrichen und Zeilenumbrüchen."
    
    def __init__(self):
        super().__init__(self.name, "WordCounterTool")
        self.input_params = {
            "text": "string",
            "count_hyphens_as_one": "boolean"
        }
    
    def execute_tool(self, input_params: dict) -> bool:
        try:
            text = input_params.get("text", "").strip()
            count_hyphens_as_one = input_params.get("count_hyphens_as_one", False)
            
            if not text:
                self.error_message = "Bitte geben Sie einen Text ein."
                return False
            
            # Replace multiple spaces and newlines with single space
            text = ' '.join(text.split())
            
            if count_hyphens_as_one:
                # Count hyphenated words as one word
                word_count = len(text.split())
            else:
                # Count hyphenated parts as separate words
                # First split by spaces to get words
                words = text.split()
                # Then split hyphenated words and count total
                word_count = sum(len(word.split('-')) for word in words)
            
            self.output = f"""
            <div class='card'>
                <div class='card-body'>
                    <h5>Ergebnis der Wortzählung:</h5>
                    <p>Anzahl der Wörter: <strong>{word_count}</strong></p>
                </div>
            </div>
            """
            return True
            
        except Exception as e:
            self.error_message = f"Ein Fehler ist aufgetreten: {str(e)}"
            return False 