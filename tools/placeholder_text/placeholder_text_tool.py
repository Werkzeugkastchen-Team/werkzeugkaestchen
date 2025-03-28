from tool_interface import MiniTool

class PlaceholderTextTool(MiniTool):
    name = "Platzhalter-Text Generator"
    description = "Platzhalter-Text Generator"

    def __init__(self):
        super().__init__("Platzhalter-Text Generator", "PlaceholderTextTool")
        self.input_params = {
            "length": {
                "name": "Textlänge",
                "type": "number",
                "required": True,
                "min": 1,
                "max": 1000,
                "placeholder": "Anzahl der Wörter (1-1000)"
            }
        }

        self.lorem_words = [
            "Lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", 
            "elit", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", 
            "et", "dolore", "magna", "aliqua", "Ut", "enim", "ad", "minim", "veniam",
            "quis", "nostrud", "exercitation", "ullamco", "laboris", "nisi", "ut",
            "aliquip", "ex", "ea", "commodo", "consequat", "Duis", "aute", "irure",
            "dolor", "in", "reprehenderit", "in", "voluptate", "velit", "esse",
            "cillum", "dolore", "eu", "fugiat", "nulla", "pariatur"
        ]

    def execute_tool(self, input_params):
        try:
            if "length" not in input_params:
                self.error_message = "Bitte geben Sie eine gültige Zahl ein."
                return False

            length = int(input_params.get("length"))

            if length <= 0 or length > 1000:
                self.error_message = "Bitte geben Sie eine Zahl zwischen 1 und 1000 ein."
                return False

            words = []
            while len(words) < length:
                words.extend(self.lorem_words[:min(length - len(words), len(self.lorem_words))])

            text = " ".join(words)
            text = text[0].upper() + text[1:]

            self.output = f"""
            <div class="generated-text-container">
                <p id="generatedText">{text}</p>
                <button onclick="copyText()" class="btn btn-secondary copy-btn">
                    <i class="fas fa-copy"></i> Kopieren
                </button>
            </div>

            <script>
            function copyText() {{
                const text = document.getElementById('generatedText').innerText;
                const copyBtn = document.querySelector('.copy-btn');
                
                navigator.clipboard.writeText(text).then(() => {{
                    copyBtn.innerHTML = '<i class="fas fa-check"></i> Kopiert!';
                    copyBtn.classList.add('btn-success');
                    copyBtn.classList.remove('btn-secondary');
                    
                    setTimeout(() => {{
                        copyBtn.innerHTML = '<i class="fas fa-copy"></i> Kopieren';
                        copyBtn.classList.remove('btn-success');
                        copyBtn.classList.add('btn-secondary');
                    }}, 2000);
                }}).catch(err => {{
                    alert('Fehler beim Kopieren: ' + err);
                }});
            }}
            </script>

            <style>
            .generated-text-container {{
                position: relative;
                margin: 20px 0;
            }}
            #generatedText {{
                font-family: Georgia, serif;
                line-height: 1.6;
                padding: 15px;
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                margin-bottom: 10px;
            }}
            .copy-btn {{
                transition: all 0.3s ease;
            }}
            .btn-success {{
                background-color: #28a745;
                border-color: #28a745;
                color: white;
            }}
            </style>
            """
            return True

        except ValueError:
            self.error_message = "Bitte geben Sie eine gültige Zahl ein."
            return False
        except Exception as e:
            self.error_message = f"Ein Fehler ist aufgetreten: {str(e)}"
            return False
