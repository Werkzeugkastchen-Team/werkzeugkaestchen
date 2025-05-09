from tool_interface import MiniTool
from datetime import datetime
import pytz
from flask_babel import lazy_gettext as _


class TimezoneConverterTool(MiniTool):
    def __init__(self):
        name = _("Zeitzonen-Konverter")
        super().__init__(name, "TimezoneConverterTool")
        self.description = _("Konvertiert Datum und Uhrzeit von einer Zeitzone in eine andere.")
        self.input_params = {
            "date": {
                "type": "string",
                "placeholder": _("TT.MM.JJJJ"),
                "required": True
            },
            "time": {
                "type": "string",
                "placeholder": _("HH:MM:SS"),
                "required": False
            },
            "from_timezone": {
                "type": "string",
                "placeholder": "Europe/Berlin",
                "required": True
            },
            "to_timezone": {
                "type": "string",
                "placeholder": "Asia/Tokyo",
                "required": True
            }
        }

    def execute_tool(self, input_params: dict) -> bool:
        try:
            date_str = input_params.get("date")
            time_str = input_params.get("time", "00:00:00")
            from_tz = input_params.get("from_timezone")
            to_tz = input_params.get("to_timezone")

            if not date_str or not from_tz or not to_tz:
                self.error_message = _("Bitte geben Sie Datum, Quell- und Zielzeitzone ein.")
                return False

            datetime_str = f"{date_str} {time_str}"
            naive_dt = datetime.strptime(datetime_str, "%d.%m.%Y %H:%M:%S")

            from_zone = pytz.timezone(from_tz)
            to_zone = pytz.timezone(to_tz)

            localized_dt = from_zone.localize(naive_dt)
            target_dt = localized_dt.astimezone(to_zone)

            self.output = f"""
                <p><strong>{_('Originalzeit')}:</strong> {localized_dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')}</p>
                <p><strong>{_('Konvertierte Zeit')}:</strong> {target_dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')}</p>
            """
            return True

        except Exception as e:
            self.error_message = _("Fehler bei der Konvertierung: %(error)s", error=str(e))
            return False
