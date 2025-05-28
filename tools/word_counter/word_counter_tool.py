from flask_babel import lazy_gettext as _
from tool_interface import MiniTool


class WordCounterTool(MiniTool):
    name = _("Wortzähler")
    description = _(
        "Zählt die Anzahl der Wörter in einem Text, unter Berücksichtigung von Bindestrichen und Zeilenumbrüchen.")

    def __init__(self):
        super().__init__(self.name, "WordCounterTool")
        self.input_params = {
            "text": "string",
            "Wörter mit Bindestrichen als einzelne Wörter zählen": "boolean"
        }

    def execute_tool(self, input_params: dict) -> bool:
        try:
            text = input_params.get("text", "").strip()
            count_hyphens_as_one = input_params.get(
                "count_hyphens_as_one", False)

            if not text:
                self.error_message = _("Bitte geben Sie einen Text ein.")
                return False

            # Mehrfache Leerzeichen und Zeilenumbrüche werden zu einem einzelnen Leerzeichen zusammengefasst.
            text = " ".join(text.split())

            if count_hyphens_as_one:
                word_count = len(text.split())
            else:
                words = text.split()
                word_count = sum(len(word.split("-")) for word in words)

            # Alle Übersetzungstexte als Variablen definieren
            header_text = _("Ergebnis der Wortzählung:")
            label_text = _("Anzahl der Wörter:")

            # HTML-Ausgabe zusammenbauen
            html_output = (
                "<div class='card'>"
                "<div class='card-body'>"
                f"<h5>{header_text}</h5>"
                f"<p>{label_text} <strong>{word_count}</strong></p>"
                "</div>"
                "</div>"
            )
            self.output = html_output
            return True

        except Exception as e:
            self.error_message = _("Ein Fehler ist aufgetreten: ") + str(e)
            return False
