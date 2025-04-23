from tool_interface import MiniTool, OutputType
from flask_babel import lazy_gettext as _

class NumberConverterTool(MiniTool):
    name = _("Zahlenkonverter")
    description = _("Konvertiert zwischen Binär-, Dezimal- und Hexadezimalzahlen.")

    def __init__(self):
        super().__init__(self.name, "NumberConverterTool")
        self.info = _(r"Geben Sie eine Zahl ein und wählen Sie den entsprechenden Zahlentyp aus. Das Tool wird die Zahl automatisch in die anderen Formate konvertieren.")
        self.input_params = {
            "number": "string",
            "input_type": "string"
        }

    def execute_tool(self, input_params: dict) -> bool:
        try:
            number = input_params.get("number", "")
            input_type = input_params.get("input_type", "")

            if not number or not input_type:
                self.error_message = _("Bitte geben Sie eine Zahl und den Zahlentyp ein.")
                return False

            # Convert input to decimal first
            decimal_num = 0
            try:
                if input_type == "binary":
                    decimal_num = int(number, 2)
                elif input_type == "decimal":
                    decimal_num = int(number)
                elif input_type == "hexadecimal":
                    decimal_num = int(number, 16)
                else:
                    self.error_message = _("Ungültiger Zahlentyp")
                    return False
            except ValueError:
                self.error_message = _("Ungültige Eingabe für den Typ %(type)s", type=input_type)
                return False

            # Convert decimal to all formats
            binary = bin(decimal_num)[2:]  # Remove '0b' prefix
            decimal = str(decimal_num)
            hexadecimal = hex(decimal_num)[2:].upper()  # Remove '0x' prefix and convert to uppercase

            title = _("Konvertierungsergebnisse:")
            binary_label = _("Binär:")
            decimal_label = _("Dezimal:")
            hex_label = _("Hexadezimal:")

            # Set output type
            # Format output
            self.output = f"""
            <div class='card'>
                <div class='card-body'>
                    <h5>{title}</h5>
                    <p><strong>{binary_label}</strong> {binary}</p>
                    <p><strong>{decimal_label}</strong> {decimal}</p>
                    <p><strong>{hex_label}</strong> {hexadecimal}</p>
                </div>
            </div>
            """
            return True

        except Exception as e:
            self.error_message = str(e)
            return False
