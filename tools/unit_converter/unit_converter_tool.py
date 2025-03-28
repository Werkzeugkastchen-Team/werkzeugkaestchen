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
                "placeholder": "z.B. length oder weight"
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
                "placeholder": "z.B. m oder kg"
            },
            "to_unit": {
                "name": "Zu Einheit",
                "type": "text",
                "required": True,
                "placeholder": "z.B. km oder g"
            }
        }

    def execute_tool(self, input_params):
        try:
            category = input_params.get("category", "").lower().strip()
            value = float(input_params.get("value", "0"))
            from_unit = input_params.get("from_unit", "").lower().strip()
            to_unit = input_params.get("to_unit", "").lower().strip()

            conversions = {
                "length": {
                    "m": 1.0,
                    "km": 0.001,
                    "cm": 100.0,
                    "mm": 1000.0
                },
                "weight": {
                    "kg": 1.0,
                    "g": 1000.0,
                    "mg": 1000000.0,
                    "t": 0.001
                }
            }

            if category not in conversions:
                self.error_message = f"Kategorie '{category}' wird nicht unterstützt"
                return False

            if from_unit not in conversions[category] or to_unit not in conversions[category]:
                self.error_message = "Unbekannte Einheit"
                return False

            try:
                base_value = value / conversions[category][from_unit]
                converted_value = base_value * conversions[category][to_unit]
                self.output = f"{value} {from_unit} = {converted_value} {to_unit}"
                return True
            except ValueError:
                self.error_message = "Ungültiger Zahlenwert"
                return False

        except ValueError:
            self.error_message = "Ungültiger Zahlenwert"
            return False
        except Exception as e:
            self.error_message = f"Ein Fehler ist aufgetreten: {str(e)}"
            return False
