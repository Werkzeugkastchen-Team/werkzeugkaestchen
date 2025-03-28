import difflib
import html
from typing import Dict, Any, List
from tool_interface import MiniTool

class TexteVergleichenTool(MiniTool):
    def __init__(self):
        super().__init__("Textvergleich", "TexteVergleichenTool")
        self.input_params = {
            "Text 1": {
                "type": "textarea"
            },
            "Text 2": {
                "type": "textarea"
            }
        }
        self.similarity_score = 0.0
        self.description = "Vergleicht zwei Texte und zeigt Unterschiede und Ähnlichkeiten zwischen ihnen (Diff)."

    def execute_tool(self, input_params: Dict[str, Any]) -> bool:
        try:
            # Eingabeparameter extrahieren
            text1 = input_params.get("Text 1", "").strip()
            text2 = input_params.get("Text 2", "").strip()

            # Eingaben validieren
            if not text1 or not text2:
                self.error_message = "Bitte geben Sie beide Texte zum Vergleich ein."
                return False

            # Ähnlichkeit berechnen
            self.similarity_score = self._calculate_similarity(text1, text2)

            # Detaillierten Vergleich generieren
            diff_results = self._generate_detailed_comparison(text1, text2)

            # HTML-Ausgabe erstellen
            result_html = self._create_interactive_html_output(
                text1, 
                text2, 
                diff_results, 
                self.similarity_score
            )

            self.output = result_html
            return True

        except Exception as e:
            self.error_message = f"Fehler beim Textvergleich: {str(e)}"
            return False

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Berechnet die Textähnlichkeit in Prozent"""
        seq_matcher = difflib.SequenceMatcher(None, text1, text2)
        return round(seq_matcher.ratio() * 100, 2)

    def _generate_detailed_comparison(self, text1: str, text2: str) -> List[Dict[str, Any]]:
        """Erstellt einen detaillierten Vergleich zwischen zwei Texten"""
        # Split while preserving line breaks
        words1 = []
        for line in text1.splitlines(keepends=True):
            if line.endswith('\n'):
                words1.extend(line[:-1].split())
                words1.append('\n')
            else:
                words1.extend(line.split())
                
        words2 = []
        for line in text2.splitlines(keepends=True):
            if line.endswith('\n'):
                words2.extend(line[:-1].split())
                words2.append('\n')
            else:
                words2.extend(line.split())
                
        matcher = difflib.SequenceMatcher(None, words1, words2)
        
        diff_results = []
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                for word in words1[i1:i2]:
                    diff_results.append({'type': 'similar', 'text': word})
            elif tag in ['delete', 'insert', 'replace']:
                if tag == 'delete':
                    for word in words1[i1:i2]:
                        diff_results.append({'type': 'different', 'text': word, 'status': 'gelöscht'})
                elif tag == 'insert':
                    for word in words2[j1:j2]:
                        diff_results.append({'type': 'different', 'text': word, 'status': 'hinzugefügt'})
                else:
                    old_words = words1[i1:i2]
                    new_words = words2[j1:j2]
                    for old_word, new_word in zip(old_words, new_words):
                        diff_results.append({
                            'type': 'different',
                            'old_text': old_word,
                            'new_text': new_word,
                            'status': 'ersetzt'
                        })
        return diff_results

    def _create_interactive_html_output(self, text1: str, text2: str, diff_results: List[Dict[str, Any]], similarity: float) -> str:
        """Erstellt eine interaktive HTML-Ausgabe für den Textvergleich"""
        similarities = []
        differences = []
        
        for diff in diff_results:
            if diff['type'] == 'similar':
                text = diff["text"]
                if text == '\n':
                    similarities.append('<br>')
                else:
                    similarities.append(f'<span class="similar">{html.escape(text)}</span> ')
            elif diff['type'] == 'different':
                if diff['status'] == 'gelöscht':
                    text = diff["text"]
                    if text == '\n':
                        differences.append('<span class="deleted">&crarr;</span><br>')
                    else:
                        differences.append(f'<span class="deleted">{html.escape(text)}</span> ')
                elif diff['status'] == 'hinzugefügt':
                    text = diff["text"]
                    if text == '\n':
                        differences.append('<span class="added">&crarr;</span><br>')
                    else:
                        differences.append(f'<span class="added">{html.escape(text)}</span> ')
                elif diff['status'] == 'ersetzt':
                    old_text = diff["old_text"]
                    new_text = diff["new_text"]
                    if old_text == '\n' or new_text == '\n':
                        old_display = "↵" if old_text == "\n" else html.escape(old_text)
                        new_display = "↵" if new_text == "\n" else html.escape(new_text)
                        differences.append(
                        f'<span class="replaced">'
                        f'<span class="replaced-old">{old_display}</span> → '
                        f'<span class="replaced-new">{new_display}</span>'
                        f'</span><br>'
                        )
                    else:
                        differences.append(
                        f'<span class="replaced">'
                        f'<span class="replaced-old">{html.escape(old_text)}</span> → '
                        f'<span class="replaced-new">{html.escape(new_text)}</span>'
                        f'</span> '
                        )

        result_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                .similar {{ color: blue; }}
                .deleted {{ color: red; text-decoration: line-through; background-color: #ffdddd; }}
                .added {{ color: green; background-color: #ddffdd; }}
                .replaced {{ background-color: #ffffcc; }}
                .replaced-old {{ color: red; text-decoration: line-through; }}
                .replaced-new {{ color: green; font-weight: bold; }}
                .view-buttons {{ margin-bottom: 15px; }}
                .view-buttons button {{ margin-right: 10px; padding: 5px 10px; }}
                .active-view {{ background-color: #007bff; color: white; }}
            </style>
        </head>
        <body>
            <div class="text-comparison-result">
                <div class="comparison-summary">
                    <h3>Ergebnisse des Textvergleichs</h3>
                    <div class="alert alert-info">
                        <strong>Vergleichsdetails:</strong>
                        <ul>
                            <li>Ähnlichkeit: {similarity}%</li>
                        </ul>
                    </div>
                </div>
                
                <div class="view-buttons">
                    <button onclick="showAll()" id="all-btn">Alles anzeigen</button>
                    <button onclick="showDifferences()" id="diff-btn">Unterschiede anzeigen</button>
                    <button onclick="showSimilarities()" id="sim-btn">Ähnlichkeiten anzeigen</button>
                </div>
                
                <div class="comparison-visualization" id="comparison-display">
                    <h4>Unterschiede und Ähnlichkeiten</h4>
                    <div class="diff-display" id="display-content">
                        {''.join(similarities + differences)}
                    </div>
                </div>
                
                <div class="original-texts row">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">Originaltext 1</div>
                            <div class="card-body">
                                <pre>{html.escape(text1)}</pre>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">Originaltext 2</div>
                            <div class="card-body">
                                <pre>{html.escape(text2)}</pre>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                const allContent = `{''.join(similarities + differences)}`;
                const differencesContent = `{''.join(differences)}`;
                const similaritiesContent = `{''.join(similarities)}`;
                const displayContent = document.getElementById('display-content');

                function showAll() {{
                    displayContent.innerHTML = allContent;
                }}

                function showDifferences() {{
                    displayContent.innerHTML = differencesContent || 'Keine Unterschiede gefunden.';
                }}

                function showSimilarities() {{
                    displayContent.innerHTML = similaritiesContent || 'Keine Ähnlichkeiten gefunden.';
                }}

                showAll();
            </script>
        </body>
        </html>
        """
        return result_html
