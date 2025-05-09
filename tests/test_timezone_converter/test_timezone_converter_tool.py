from datetime import datetime
import pytz
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from tool_interface import MiniTool


class TimezoneConverterTool(MiniTool):
    def __init__(self):
        self.name = "Zeitzonen-Rechner"
        self.description = "Gibt eine Uhrzeit in anderen Zeitzonen aus."
        self.identifier = "TimezoneConverterTool"
        self.use_cases = [
            "Vergleich von Zeiten in verschiedenen Ländern",
            "Meeting-Planung über Zeitzonen hinweg",
            "Weltzeit anzeigen"
        ]
        self.output = ""
        self.error_message = ""
        self.input_params = {
            "input_time": "string",           
            "source_zone": "string",
            "target_zone": "string"          
        }

    def process(self, form):
        input_time = form.get("input_time", "")
        source_zone = form.get("source_zone", "")
        target_zone = form.get("target_zone", "all")

        try:
            dt = datetime.strptime(input_time, "%H:%M")
            now = datetime.now()
            dt = dt.replace(year=now.year, month=now.month, day=now.day)

            if source_zone not in pytz.all_timezones:
                return {"error": f"Unbekannte Quell-Zeitzone: {source_zone}"}

            source_tz = pytz.timezone(source_zone)
            localized_dt = source_tz.localize(dt)

            if not target_zone or target_zone == "all":
                zones = pytz.all_timezones
            else:
                if target_zone not in pytz.all_timezones:
                    return {"error": f"Unbekannte Ziel-Zeitzone: {target_zone}"}
                zones = [target_zone]

            results = []
            for zone in zones:
                target_tz = pytz.timezone(zone)
                converted = localized_dt.astimezone(target_tz)
                results.append(f"{zone}: {converted.strftime('%H:%M')}")

            return "<br>".join(results)

        except Exception as e:
            return {"error": f"Ungültiges Zeitformat. Bitte HH:MM angeben. ({str(e)})"}

    def execute_tool(self, input_params):
        result = self.process(input_params)
        if isinstance(result, dict) and "error" in result:
            self.error_message = result["error"]
            return False
        self.output = result
        return True
