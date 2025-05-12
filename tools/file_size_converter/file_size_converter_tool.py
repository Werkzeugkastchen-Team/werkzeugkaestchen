# filepath: c:\Users\David\PycharmProjects\werkzeugkaestchen\tools\file_size_converter\file_size_converter_tool.py
from tool_interface import MiniTool, OutputType
from flask_babel import lazy_gettext as _


class FileSizeConverterTool(MiniTool):
    def __init__(self):
        # Übersetzungsvariablen
        tool_title = _("Dateigrößen-Konverter")
        tool_desc = _("Konvertiert Dateigrößen zwischen verschiedenen Einheiten (Bytes, KB, MB, GB, TB)")
        super().__init__(tool_title, "FileSizeConverterTool")
        self.description = tool_desc
        self.output_type = OutputType.TEXT
        self.input_params = {
            "size": {
                "label": _("Größe"),
                "type": "number",
                "required": True,
                "step": "any"
            },
            "unit": {
                "label": _("Einheit"),
                "type": "select",
                "options": [
                    {"value": "bytes", "label": _("Bytes")},
                    {"value": "kb", "label": _("Kilobyte (KB)")},
                    {"value": "mb", "label": _("Megabyte (MB)")},
                    {"value": "gb", "label": _("Gigabyte (GB)")},
                    {"value": "tb", "label": _("Terabyte (TB)")},
                    {"value": "kib", "label": _("Kibibyte (KiB)")},
                    {"value": "mib", "label": _("Mebibyte (MiB)")},
                    {"value": "gib", "label": _("Gibibyte (GiB)")},
                    {"value": "tib", "label": _("Tebibyte (TiB)")}
                ],
                "required": True
            }
        }

    def execute_tool(self, input_params: dict) -> bool:
        try:
            # Eingabeparameter erhalten
            size = float(input_params.get("size", 0))
            unit = input_params.get("unit", "bytes")
            
            # Umrechnung in Bytes
            bytes_value = self._convert_to_bytes(size, unit)
            
            # Umrechnung in andere Einheiten
            result = self._convert_from_bytes(bytes_value)
            
            # Text-Ausgabe erstellen
            self.output = self._create_output(result, size, unit)
            return True
            
        except Exception as e:
            self.error_message = _("Fehler bei der Umrechnung: ") + str(e)
            return False
    
    def _convert_to_bytes(self, size, unit):
        """Konvertiert eine Größe in die Einheit Bytes"""
        if unit == "bytes":
            return size
        elif unit == "kb":
            return size * 1000
        elif unit == "mb":
            return size * 1000 * 1000
        elif unit == "gb":
            return size * 1000 * 1000 * 1000
        elif unit == "tb":
            return size * 1000 * 1000 * 1000 * 1000
        elif unit == "kib":
            return size * 1024
        elif unit == "mib":
            return size * 1024 * 1024
        elif unit == "gib":
            return size * 1024 * 1024 * 1024
        elif unit == "tib":
            return size * 1024 * 1024 * 1024 * 1024
        return 0
    
    def _convert_from_bytes(self, bytes_value):
        """Konvertiert Bytes in verschiedene Einheiten"""
        result = {
            "bytes": bytes_value,
            "kb": bytes_value / 1000,
            "mb": bytes_value / (1000 * 1000),
            "gb": bytes_value / (1000 * 1000 * 1000),
            "tb": bytes_value / (1000 * 1000 * 1000 * 1000),
            "kib": bytes_value / 1024,
            "mib": bytes_value / (1024 * 1024),
            "gib": bytes_value / (1024 * 1024 * 1024),
            "tib": bytes_value / (1024 * 1024 * 1024 * 1024)
        }
        return result
    
    def _create_output(self, result, original_size, original_unit):
        """Erstellt eine Text-Ausgabe mit den Umrechnungsergebnissen"""
        # Übersetzbare Texte
        msg_original = _("Originalgröße")
        msg_decimal = _("Dezimale Einheiten (SI)")
        msg_binary = _("Binäre Einheiten (IEC)")
        
        # Beschreibungen für jede Einheit
        descriptions = {
            "bytes": _("Bytes"),
            "kb": _("Kilobyte (1000 Bytes)"),
            "mb": _("Megabyte (1000 KB)"),
            "gb": _("Gigabyte (1000 MB)"),
            "tb": _("Terabyte (1000 GB)"),
            "kib": _("Kibibyte (1024 Bytes)"),
            "mib": _("Mebibyte (1024 KiB)"),
            "gib": _("Gibibyte (1024 MiB)"),
            "tib": _("Tebibyte (1024 GiB)")
        }
        
        # Menschenlesbare Einheitsnamen
        unit_names = {
            "bytes": _("Bytes"),
            "kb": _("KB"),
            "mb": _("MB"),
            "gb": _("GB"),
            "tb": _("TB"),
            "kib": _("KiB"),
            "mib": _("MiB"),
            "gib": _("GiB"),
            "tib": _("TiB")
        }
        
        # Text-Ausgabe erstellen
        output_text = f"{msg_original}: {original_size} {unit_names[original_unit]}\n\n"
        
        output_text += f"{msg_decimal}\n"
        output_text += f"- Bytes: {result['bytes']:,.0f} ({descriptions['bytes']})\n"
        output_text += f"- KB: {result['kb']:,.3f} ({descriptions['kb']})\n"
        output_text += f"- MB: {result['mb']:,.3f} ({descriptions['mb']})\n"
        output_text += f"- GB: {result['gb']:,.3f} ({descriptions['gb']})\n"
        output_text += f"- TB: {result['tb']:,.3f} ({descriptions['tb']})\n\n"
        
        output_text += f"{msg_binary}\n"
        output_text += f"- KiB: {result['kib']:,.3f} ({descriptions['kib']})\n"
        output_text += f"- MiB: {result['mib']:,.3f} ({descriptions['mib']})\n"
        output_text += f"- GiB: {result['gib']:,.3f} ({descriptions['gib']})\n"
        output_text += f"- TiB: {result['tib']:,.3f} ({descriptions['tib']})\n"
        
        return output_text