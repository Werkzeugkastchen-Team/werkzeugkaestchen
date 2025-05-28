from datetime import datetime
from tool_interface import MiniTool
from flask_babel import lazy_gettext as _

class CalendarWeekTool(MiniTool):
    name = _("Kalenderwochenberechner")
    description = _("Berechnet die Kalenderwoche für ein gegebenes Datum (Format: TT.MM.JJJJ).")

    def __init__(self):
        super().__init__(self.name, "CalendarWeekTool")
        self.input_params = {
            _("Datum"): "date"
        }

    def execute_tool(self, input_params: dict) -> bool:
        try:
            # Wir verwenden den übersetzten Schlüssel, der in input_params ankommen könnte
            # oder den nicht-übersetzten Schlüssel als Fallback
            date_str = None
            for key in input_params:
                if key == _("Datum") or key == "Datum":
                    date_str = input_params[key].strip()
                    break
            
            if not date_str:
                self.error_message = _("Bitte geben Sie ein Datum ein.")
                return False

            # Versuche, das Datum zu parsen, und behandle verschiedene gängige Formate
            try:
                # Versuche zuerst das Format TT.MM.JJJJ
                date_obj = datetime.strptime(date_str, "%d.%m.%Y")
            except ValueError:
                try:
                    # Versuche das Format YYYY-MM-DD (von HTML input type="date")
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    try:
                        # Versuche alternatives Format mit einstelligen Tagen/Monaten (für TT.MM.JJJJ)
                        date_parts = date_str.split('.')
                        if len(date_parts) == 3:
                            day = date_parts[0].zfill(2)
                            month = date_parts[1].zfill(2)
                            year = date_parts[2].zfill(4)
                            date_obj = datetime.strptime(f"{day}.{month}.{year}", "%d.%m.%Y")
                        else:
                            raise ValueError("Ungültige Anzahl von Teilen im Datum")
                    except ValueError:
                        self.error_message = _(
                            "Ungültiges Datumsformat. Bitte verwenden Sie das Format TT.MM.JJJJ oder YYYY-MM-DD.")
                        return False

            # Berechne die Kalenderwoche
            calendar_data = date_obj.isocalendar()
            year, week, day_of_week = calendar_data

            msg_title = _("Kalenderwochenberechnung:")
            msg_date = _("Das Datum")
            msg_is_in = _("liegt in:")
            msg_cw = _("KW")
            msg_in_year = _("im Jahr")

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
