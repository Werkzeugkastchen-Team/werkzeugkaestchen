from flask_babel import lazy_gettext as _
from tool_interface import MiniTool
from datetime import datetime

class DateCalculatorTool(MiniTool):
    def __init__(self):
        super().__init__(_("Datumsrechner"), "DateCalculatorTool")
        self.description = _("Berechnet den Unterschied zwischen zwei Daten in Tagen.")
        self.input_params = {
            _('Startdatum'): "date",
            _('Enddatum'): "date"
        }

    def execute_tool(self, input_params):
        try:
            start_date = input_params.get(_('Startdatum'), '').strip()
            end_date = input_params.get(_('Enddatum'), '').strip()

            is_valid_start, start_date_obj, start_error = self.validate_date(start_date)
            if not is_valid_start:
                self.error_message = start_error
                return False

            is_valid_end, end_date_obj, end_error = self.validate_date(end_date)
            if not is_valid_end:
                self.error_message = end_error
                return False

            difference = abs((end_date_obj - start_date_obj).days)

            self.output = _("Die Differenz beträgt <strong>{0}</strong> Tage.").format(difference)
            return True

        except Exception as e:
            self.error_message = _("Ein Fehler ist aufgetreten:") + f" {str(e)}"
            return False

    def validate_date(self, date_str):
        if not date_str:
            return False, None, _("Bitte geben Sie ein gültiges Datum ein.")
        try:
            date_obj = datetime.strptime(date_str, '%d.%m.%Y')
        except ValueError:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                return False, None, _("Bitte geben Sie ein gültiges Datum im Format TT.MM.JJJJ oder YYYY-MM-DD ein.")
        
        if date_obj.year < 1900:
            return False, None, _("Jahresangaben müssen ab 1900 sein.")
        return True, date_obj, ""
