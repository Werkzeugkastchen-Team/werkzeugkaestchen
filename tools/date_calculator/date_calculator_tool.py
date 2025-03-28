from tool_interface import MiniTool
from datetime import datetime

class DateCalculatorTool(MiniTool):
    def __init__(self):
        super().__init__("Datumsrechner", "DateCalculatorTool")
        self.description = "Berechnet den Unterschied zwischen zwei Daten in Tagen."
        self.input_params = {
            'start_date': {
                'name': 'Startdatum',
                'type': 'text',
                'required': True,
                'placeholder': 'DD.MM.YYYY'
            },
            'end_date': {
                'name': 'Enddatum',
                'type': 'text',
                'required': True,
                'placeholder': 'DD.MM.YYYY'
            }
        }

    def execute_tool(self, input_params):
        try:
            start_date = input_params.get('start_date', '').strip()
            end_date = input_params.get('end_date', '').strip()

            is_valid_start, start_date_obj, start_error = self.validate_date(start_date)
            if not is_valid_start:
                self.error_message = start_error
                return False

            is_valid_end, end_date_obj, end_error = self.validate_date(end_date)
            if not is_valid_end:
                self.error_message = end_error
                return False

            difference = abs((end_date_obj - start_date_obj).days)

            self.output = f"Die Differenz beträgt <strong>{difference}</strong> Tage."
            return True

        except Exception as e:
            self.error_message = f"Ein Fehler ist aufgetreten: {str(e)}"
            return False

    def validate_date(self, date_str):
        if not date_str:
            return False, None, "Bitte geben Sie ein gültiges Datum ein."
        try:
            date_obj = datetime.strptime(date_str, '%d.%m.%Y')
            if date_obj.year < 1900:
                return False, None, "Jahresangaben müssen ab 1900 sein."
            return True, date_obj, ""
        except ValueError:
            return False, None, "Bitte geben Sie ein gültiges Datum im Format DD.MM.YYYY ein."
