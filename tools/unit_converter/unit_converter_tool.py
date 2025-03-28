from tool_interface import MiniTool

class UnitConverterTool(MiniTool):
    def __init__(self):
        super().__init__("Einheitenrechner", "UnitConverterTool")
        self.description = "Rechnet Einheiten wie Längen oder Gewichte um. Die Eingabemaske passt sich der Kategorie an."
        self.input_params = {
            "category": {
                "name": "Kategorie",
                "type": "text",
                "required": True,
                "placeholder": "z.B. Länge oder Gewicht"
            },
            "value": {
                "name": "Wert",
                "type": "text",
                "required": True,
                "placeholder": "z.B. 10"
            },
            "from_unit": {
                "name": "Von Einheit",
                "type": "text",
                "required": True,
                "placeholder": "z.B. Meter oder Kilogramm"
            },
            "to_unit": {
                "name": "Zu Einheit",
                "type": "text",
                "required": True,
                "placeholder": "z.B. Zentimeter oder Gramm"
            }
        }

    def execute_tool(self, input_params):
        try:
            category = input_params.get("category", "").lower().strip()
            value = float(input_params.get("value", "0"))
            from_unit = input_params.get("from_unit", "").lower().strip()
            to_unit = input_params.get("to_unit", "").lower().strip()

            conversions = {
                "länge": {
                    "meter": 1.0,
                    "zentimeter": 100.0,
                    "millimeter": 1000.0,
                    "kilometer": 0.001,
                    "inch": 39.3701,
                    "fuß": 3.28084
                },
                "gewicht": {
                    "kilogramm": 1.0,
                    "gramm": 1000.0,
                    "milligramm": 1000000.0,
                    "tonne": 0.001,
                    "pfund": 2.20462,
                    "unze": 35.274
                }
            }

            if category not in conversions:
                self.error_message = "Ungültige Kategorie. Bitte 'Länge' oder 'Gewicht' verwenden."
                return False

            if from_unit not in conversions[category] or to_unit not in conversions[category]:
                self.error_message = "Ungültige Einheit für gewählte Kategorie."
                return False

            base_value = value / conversions[category][from_unit]
            converted_value = base_value * conversions[category][to_unit]

            self.output = f"{value} {from_unit} = {converted_value:.4f} {to_unit}"
            return True

        except ValueError:
            self.error_message = "Bitte geben Sie einen gültigen numerischen Wert ein."
            return False
        except Exception as e:
            self.error_message = f"Ein Fehler ist aufgetreten: {str(e)}"
            return False
