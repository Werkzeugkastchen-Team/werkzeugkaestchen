from datetime import datetime
from tool_interface import MiniTool
from flask_babel import lazy_gettext as _

# Dieses Werkzeug hat so viele nerfen gekostet weil input_params nur Probleme macht für die Übersetzung
# Ich weiß jeder der diesen Code sehen wird, wird Automatisch Probleme Persönlich mit mir bekommen
# Aber ich habe keine Lust mehr auf diese Scheiße

class CalendarWeekTool(MiniTool):
    name = _("Kalenderwochenberechner")
    description = _("Berechnet die Kalenderwoche für ein gegebenes Datum (Format: TT.MM.JJJJ).")

    def __init__(self):
        super().__init__(self.name, "CalendarWeekTool")
        self.info = _(r"Geben Sie ein Datum im Format <strong>TT.MM.JJJJ</strong> ein (z.B. 15.03.2025), um die entsprechende Kalenderwoche zu berechnen.")
        self.input_params = {
            _("Datum"): "string"
        }

    def execute_tool(self, input_params: dict) -> bool:
        try:
            # Debug-Ausgabe hinzufügen
            print(f"Typ von _: {type(_)}")

            self.input_params = {
                "Datum": "string"
            }
            date_str = input_params.get("Datum", "")

            if not date_str:
                self.error_message = _("Bitte geben Sie ein Datum ein.")
                return False

            # Weitere Debug-Ausgaben
            print(f"Input datum: {date_str}")

            try:
                date_obj = datetime.strptime(date_str, "%d.%m.%Y")
                print(f"Parsed date: {date_obj}")
            except ValueError:
                self.error_message = _(
                    "Ungültiges Datumsformat. Bitte verwenden Sie das Format TT.MM.JJJJ (z.B. 01.12.2025).")
                return False

            # Berechne die Kalenderwoche
            calendar_data = date_obj.isocalendar()
            print(f"Calendar data: {calendar_data}, type: {type(calendar_data)}")
            year, week, day_of_week = calendar_data  # oder year, week, __ = calendar_data

            msg_title = _("Kalenderwochenberechnung:")
            msg_date = _("Das Datum")
            msg_is_in = _("liegt in:")
            msg_cw = _("KW")
            msg_in_year = _("im Jahr")

            # Dann die Variablen im f-string verwenden
            self.output = f"""
            <div class='card'>
                <div class='card-body'>
                    <h5>{msg_title}</h5>
                    <p>{msg_date} <strong>{date_str}</strong> {msg_is_in}</p>
                    <p class="display-4 text-center">{msg_cw} {week}</p>
                    <p class="text-center">{msg_in_year} {year}</p>
                </div>
            </div>
            """
            return True

        except Exception as e:
            self.error_message = f"Ein Fehler ist aufgetreten: {str(e)}"
            return False
