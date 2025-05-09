from flask_babel import lazy_gettext as _
from tool_interface import MiniTool

class UnitConverterTool(MiniTool):
    def __init__(self):
        super().__init__(_("Einheitenrechner"), "UnitConverterTool")
        self.description = _("Rechnet Einheiten wie Längen oder Gewichte um. Die Eingabemaske passt sich der Kategorie an.")
        self.input_params = {
            _("Kategorie"): {
                "type": "text",
                "required": True,
                "placeholder": _("z.B. länge oder gewicht")
            },
            _("Wert"): {
                "type": "text",
                "required": True,
                "placeholder": _("z.B. 10")
            },
            _("Von Einheit"): {
                "type": "text",
                "required": True,
                "placeholder": _("z.B. m oder kg")
            },
            _("Zu Einheit"): {
                "type": "text",
                "required": True,
                "placeholder": _("z.B. km oder g")
            }
        }

    def execute_tool(self, input_params):
        try:
            # Check for both translated keys and untranslated keys
            raw_category = input_params.get(_("Kategorie"), input_params.get("category", "")).lower().strip()
            raw_value = input_params.get(_("Wert"), input_params.get("value", "0")).strip()
            raw_from = input_params.get(_("Von Einheit"), input_params.get("from_unit", "")).lower().strip()
            raw_to = input_params.get(_("Zu Einheit"), input_params.get("to_unit", "")).lower().strip()

            # Map German/English synonyms
            category_map = {
                "länge": "length",
                "length": "length",
                "gewicht": "weight",
                "weight": "weight"
            }

            unit_map = {
                "meter": "m", "m": "m",
                "kilometer": "km", "km": "km",
                "zentimeter": "cm", "cm": "cm",
                "millimeter": "mm", "mm": "mm",
                "kilogramm": "kg", "kg": "kg",
                "gramm": "g", "g": "g",
                "milligramm": "mg", "mg": "mg",
                "tonne": "t", "t": "t"
            }

            category = category_map.get(raw_category)
            from_unit = unit_map.get(raw_from)
            to_unit = unit_map.get(raw_to)

            if category is None:
                self.error_message = _("Kategorie '{0}' wird nicht unterstützt").format(raw_category)
                return False

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

            if from_unit not in conversions[category] or to_unit not in conversions[category]:
                self.error_message = _("Unbekannte Einheit")
                return False

            try:
                value = float(raw_value)
            except ValueError:
                self.error_message = _("Ungültiger Zahlenwert")
                return False

            base_value = value / conversions[category][from_unit]
            converted_value = base_value * conversions[category][to_unit]
            self.output = f"{value} {raw_from} = {converted_value} {raw_to}"
            return True

        except Exception as e:
            self.error_message = _("Ein Fehler ist aufgetreten:") + f" {str(e)}"
            return False
