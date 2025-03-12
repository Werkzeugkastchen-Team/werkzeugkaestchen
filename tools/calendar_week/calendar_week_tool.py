from datetime import datetime
from tool_interface import MiniTool


class CalendarWeekTool(MiniTool):
    name = "Kalenderwochenberechner"
    description = "Berechnet die Kalenderwoche für ein gegebenes Datum (Format: TT.MM.JJJJ)."

    def __init__(self):
        super().__init__(self.name, "CalendarWeekTool")
        self.input_params = {
            "date": "string"
        }

    def execute_tool(self, input_params: dict) -> bool:
        try:
            date_str = input_params.get("date", "")

            if not date_str:
                self.error_message = "Bitte geben Sie ein Datum ein."
                return False

            # Versuche das Datum zu parsen (Format: TT.MM.JJJJ)
            try:
                date_obj = datetime.strptime(date_str, "%d.%m.%Y")
            except ValueError:
                self.error_message = "Ungültiges Datumsformat. Bitte verwenden Sie das Format TT.MM.JJJJ (z.B. 01.12.2025)."
                return False

            # Berechne die Kalenderwoche
            year, week, _ = date_obj.isocalendar()

            # Erstelle eine formatierte Ausgabe
            self.output = f"""
            <div class='card'>
                <div class='card-body'>
                    <h5>Kalenderwochenberechnung:</h5>
                    <p>Das Datum <strong>{date_str}</strong> liegt in:</p>
                    <p class="display-4 text-center">KW {week}</p>
                    <p class="text-center">im Jahr {year}</p>
                </div>
            </div>
            """
            return True

        except Exception as e:
            self.error_message = f"Ein Fehler ist aufgetreten: {str(e)}"
            return False