from datetime import datetime
import pytz
from tool_interface import MiniTool


class UnixTimestampTool(MiniTool):
    name = "Unix-Timestamp Konverter"
    description = "Konvertiert Unix-Timestamps in lesbare Datums- und Zeitformate und umgekehrt. Mit Unterstützung für verschiedene Zeitzonen."

    # Common timezones for the dropdow/easy to add more if needed
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
            conversion_type = input_params.get(
                "conversion_type", "timestamp_to_date")
            timezone_str = input_params.get("timezone", "UTC")

            # Try to get the timezone
            try:
                tz = pytz.timezone(timezone_str)
            except pytz.exceptions.UnknownTimeZoneError:
                self.error_message = f"Unbekannte Zeitzone: {timezone_str}"
                return False

            if conversion_type == "timestamp_to_date":
                return self._timestamp_to_date(input_params, tz)
            else:
                return self._date_to_timestamp(input_params, tz)

        except Exception as e:
            self.error_message = f"Ein Fehler ist aufgetreten: {str(e)}"
            return False

    def _timestamp_to_date(self, input_params: dict, tz) -> bool:
        # Get timestamp from input
        timestamp_str = input_params.get("timestamp", "").strip()

        if not timestamp_str:
            self.error_message = "Bitte geben Sie einen Unix-Timestamp ein."
            return False

        # Try to convert the timestamp to an integer
        try:
            timestamp = int(timestamp_str)
        except ValueError:
            self.error_message = "Der eingegebene Wert ist kein gültiger Unix-Timestamp. Bitte geben Sie eine ganze Zahl ein."
            return False

        # Validate timestamp range
        if timestamp < 0:
            self.error_message = "Negative Timestamps werden nicht unterstützt."
            return False

        if timestamp > 253402300799:  # Maximum valid timestamp (Year 9999)
            self.error_message = "Der Timestamp ist zu groß. Bitte geben Sie einen gültigen Timestamp ein."
            return False

        # Convert timestamp to datetime in UTC
        dt_utc = datetime.utcfromtimestamp(timestamp)

        # Convert to the specified timezone
        dt_local = pytz.utc.localize(dt_utc).astimezone(tz)

        # Format the output
        formatted_date = dt_local.strftime("%d.%m.%Y")
        formatted_time = dt_local.strftime("%H:%M:%S")
        formatted_timezone = tz.zone

        # Create user-friendly output
        self.output = f"""
        <div class='card'>
            <div class='card-body'>
                <h5>Konvertierungsergebnis:</h5>
                <table class="table table-striped">
                    <tr>
                        <td><strong>Unix-Timestamp:</strong></td>
                        <td>{timestamp}</td>
                    </tr>
                    <tr>
                        <td><strong>Datum:</strong></td>
                        <td>{formatted_date}</td>
                    </tr>
                    <tr>
                        <td><strong>Uhrzeit:</strong></td>
                        <td>{formatted_time}</td>
                    </tr>
                    <tr>
                        <td><strong>Zeitzone:</strong></td>
                        <td>{formatted_timezone}</td>
                    </tr>
                </table>
            </div>
        </div>
        """
        return True

    def _date_to_timestamp(self, input_params: dict, tz) -> bool:
        # Get date and time from input
        date_str = input_params.get("date", "").strip()
        time_str = input_params.get("time", "00:00:00").strip()

        if not date_str:
            self.error_message = "Bitte geben Sie ein Datum ein."
            return False

        # Try to parse the date (format: DD.MM.YYYY)
        try:
            day, month, year = map(int, date_str.split('.'))

            # Validate date components
            if not (1 <= day <= 31 and 1 <= month <= 12 and 1 <= year <= 9999):
                self.error_message = "Ungültiges Datum. Bitte verwenden Sie das Format TT.MM.JJJJ"
                return False

            # Parse time (format: HH:MM:SS or HH:MM)
            if time_str:
                time_parts = time_str.split(':')
                if len(time_parts) == 2:
                    hour, minute = map(int, time_parts)
                    second = 0
                elif len(time_parts) == 3:
                    hour, minute, second = map(int, time_parts)
                else:
                    self.error_message = "Ungültiges Zeitformat. Bitte verwenden Sie HH:MM oder HH:MM:SS"
                    return False

                # Validate time components
                if not (0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59):
                    self.error_message = "Ungültige Uhrzeit."
                    return False
            else:
                hour, minute, second = 0, 0, 0

            # Create datetime object
            dt = datetime(year, month, day, hour, minute, second)

            # Localize with the specified timezone
            dt_localized = tz.localize(dt)

            # Convert to UTC for timestamp
            dt_utc = dt_localized.astimezone(pytz.UTC)

            # Get Unix timestamp
            timestamp = int(dt_utc.timestamp())

            # Format the output
            self.output = f"""
            <div class='card'>
                <div class='card-body'>
                    <h5>Konvertierungsergebnis:</h5>
                    <table class="table table-striped">
                        <tr>
                            <td><strong>Datum:</strong></td>
                            <td>{date_str}</td>
                        </tr>
                        <tr>
                            <td><strong>Uhrzeit:</strong></td>
                            <td>{time_str}</td>
                        </tr>
                        <tr>
                            <td><strong>Zeitzone:</strong></td>
                            <td>{tz.zone}</td>
                        </tr>
                        <tr>
                            <td><strong>Unix-Timestamp:</strong></td>
                            <td>{timestamp}</td>
                        </tr>
                    </table>
                </div>
            </div>
            """
            return True

        except ValueError:
            self.error_message = "Ungültiges Datumsformat. Bitte verwenden Sie das Format TT.MM.JJJJ"
            return False
