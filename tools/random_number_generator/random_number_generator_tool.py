from tool_interface import MiniTool
import random
import sys
from flask_babel import lazy_gettext as _


class RandomNumberGeneratorTool(MiniTool):
    name = _("Zufallszahlengenerator")
    description = _("Generiere eine Zufallszahl. Beispiel: Nenne mit eine Zahl zwischen 1 und 10")

    def __init__(self):
        super().__init__(self.name, "RandomNumberGeneratorTool")
        min_number = _("Minimum Number")
        max_number = _("Maximum Number")
        amount_rolls = _("Amount of Rolls")

        self.input_params = {
            min_number: "string",
            max_number: "string",
            amount_rolls: "string"
        }

    def execute_tool(self, input_params: dict) -> bool:
        try:
            # Übersetzungsstrings für Eingabeparameter
            min_number = _("Minimum Number")
            max_number = _("Maximum Number")
            amount_rolls = _("Amount of Rolls")

            if not input_params.get(min_number) or not input_params.get(max_number) or not input_params.get(
                    amount_rolls):
                error_msg = _("Alle Eingabefelder müssen ausgefüllt sein.")
                self.error_message = error_msg
                return False

            min = int(input_params.get(min_number, ""))
            max = int(input_params.get(max_number, ""))
            amount_of_rolls = int(input_params.get(amount_rolls, ""))

            if not min or not max or not amount_of_rolls:
                error_msg = _("Bitte geben Sie ganze Zahlen in alle Eingabefelder ein.")
                self.error_message = error_msg
                return False

            if min > max:
                error_msg = _("Das Minimum darf nicht größer als das Maximum sein.")
                self.error_message = error_msg
                return False

            if min > sys.maxsize or max > sys.maxsize or min < -sys.maxsize:
                error_msg = _("Zahl zu hoch.")
                self.error_message = error_msg
                return False

            if amount_of_rolls > 1000:
                error_msg = _("Anzahl Würfe zu hoch.")
                self.error_message = error_msg
                return False

            random_numbers = [str(random.randint(min, max)) for _ in range(amount_of_rolls)]
            self.output = ", ".join(random_numbers)

            return True
        except Exception as e:
            self.error_message = str(e)
            return False