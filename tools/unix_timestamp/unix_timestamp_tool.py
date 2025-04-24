from datetime import datetime
import pytz
from tool_interface import MiniTool
from flask_babel import lazy_gettext as _

class UnixTimestampTool(MiniTool):
    name = _("Unix\-Timestamp Konverter")
    description = _("Konvertiert Unix\-Timestamps in lesbare Datums\- und Zeitformate und umgekehrt\. Mit Unterstützung für verschiedene Zeitzonen\.")

    COMMON_TIMEZONES = [
        "UTC", "Europe/Berlin", "Europe/London", "America/New_York",
        "America/Los_Angeles", "Asia/Tokyo", "Australia/Sydney"
    ]

    def __init__(self):
        super().__init__(self.name, "UnixTimestampTool")
        self.input_params = {
            "conversion_type": {
                "type": "enum",
                "options": ["timestamp_to_date", "date_to_timestamp"]
            },
            "timestamp": "string",
            "date": "string",
            "time": "string",
            "timezone": {
                "type": "enum",
                "options": self.COMMON_TIMEZONES
            }
        }

    def execute_tool(self, input_params: dict) -> bool:
        try:
            conversion_type = input_params.get("conversion_type", "timestamp_to_date")
            timezone_str = input_params.get("timezone", "UTC")
            try:
                tz = pytz.timezone(timezone_str)
            except pytz.exceptions.UnknownTimeZoneError:
                self.error_message = _("Unbekannte Zeitzone: %(zone)s", zone=timezone_str)
                return False

            if conversion_type == "timestamp_to_date":
                return self._timestamp_to_date(input_params, tz)
            return self._date_to_timestamp(input_params, tz)

        except Exception as e:
            self.error_message = _("Ein Fehler ist aufgetreten: %(error)s", error=str(e))
            return False

    def _timestamp_to_date(self, input_params: dict, tz) -> bool:
        timestamp_str = input_params.get("timestamp", "").strip()
        if not timestamp_str:
            self.error_message = _("Bitte geben Sie einen Unix\-Timestamp ein\.")
            return False

        try:
            timestamp = int(timestamp_str)
        except ValueError:
            self.error_message = _("Der eingegebene Wert ist kein gültiger Unix\-Timestamp\. Bitte geben Sie eine ganze Zahl ein\.")
            return False

        if timestamp < 0:
            self.error_message = _("Negative Timestamps werden nicht unterstützt\.")
            return False
        if timestamp > 253402300799:
            self.error_message = _("Der Timestamp ist zu groß\. Bitte geben Sie einen gültigen Timestamp ein\.")
            return False

        dt_utc = datetime.utcfromtimestamp(timestamp)
        dt_local = pytz.utc.localize(dt_utc).astimezone(tz)

        title          = _("Konvertierungsergebnis:")
        ts_label       = _("Unix\-Timestamp:")
        date_label     = _("Datum:")
        time_label     = _("Uhrzeit:")
        zone_label     = _("Zeitzone:")

        formatted_date = dt_local.strftime("%d.%m.%Y")
        formatted_time = dt_local.strftime("%H:%M:%S")
        formatted_zone = tz.zone

        self.output = f"""
        <div class='card'>
            <div class='card-body'>
                <h5>{title}</h5>
                <table class='table table-striped'>
                    <tr><td><strong>{ts_label}</strong></td><td>{timestamp}</td></tr>
                    <tr><td><strong>{date_label}</strong></td><td>{formatted_date}</td></tr>
                    <tr><td><strong>{time_label}</strong></td><td>{formatted_time}</td></tr>
                    <tr><td><strong>{zone_label}</strong></td><td>{formatted_zone}</td></tr>
                </table>
            </div>
        </div>
        """
        return True

    def _date_to_timestamp(self, input_params: dict, tz) -> bool:
        date_str = input_params.get("date", "").strip()
        time_str = input_params.get("time", "00:00:00").strip()

        if not date_str:
            self.error_message = _("Bitte geben Sie ein Datum ein\.")
            return False

        try:
            day, month, year = map(int, date_str.split('.'))
            if not (1 <= day <= 31 and 1 <= month <= 12 and 1 <= year <= 9999):
                raise ValueError

            parts = time_str.split(':')
            if len(parts) == 2:
                hour, minute = map(int, parts); second = 0
            elif len(parts) == 3:
                hour, minute, second = map(int, parts)
            else:
                self.error_message = _("Ungültiges Zeitformat\. Bitte verwenden Sie HH:MM oder HH:MM:SS")
                return False

            if not (0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59):
                self.error_message = _("Ungültige Uhrzeit\.")
                return False

            dt = datetime(year, month, day, hour, minute, second)
        except ValueError:
            self.error_message = _("Ungültiges Datumsformat\. Bitte verwenden Sie das Format TT\.MM\.JJJJ")
            return False

        dt_localized = tz.localize(dt)
        timestamp = int(dt_localized.astimezone(pytz.UTC).timestamp())

        title          = _("Konvertierungsergebnis:")
        date_label     = _("Datum:")
        time_label     = _("Uhrzeit:")
        zone_label     = _("Zeitzone:")
        ts_label       = _("Unix\-Timestamp:")

        self.output = f"""
        <div class='card'>
            <div class='card-body'>
                <h5>{title}</h5>
                <table class='table table-striped'>
                    <tr><td><strong>{date_label}</strong></td><td>{date_str}</td></tr>
                    <tr><td><strong>{time_label}</strong></td><td>{time_str}</td></tr>
                    <tr><td><strong>{zone_label}</strong></td><td>{tz.zone}</td></tr>
                    <tr><td><strong>{ts_label}</strong></td><td>{timestamp}</td></tr>
                </table>
            </div>
        </div>
        """
        return True