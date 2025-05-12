import os
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
            "input_type": {
                "label": _("Eingabetyp"),
                "type": "select",
                "options": [
                    {"value": "manual", "label": _("Manuelle Eingabe")},
                    {"value": "file", "label": _("Datei hochladen")}
                ],
                "required": True
            },
            "size": {
                "label": _("Größe"),
                "type": "number",
                "required": False,
                "step": "any",
                "depends_on": {"input_type": "manual"}
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
                    {"value": "kib", "label": _("Kibibyte (KiB)")},                    {"value": "mib", "label": _("Mebibyte (MiB)")},
                    {"value": "gib", "label": _("Gibibyte (GiB)")},
                    {"value": "tib", "label": _("Tebibyte (TiB)")}
                ],
                "required": False,
                "depends_on": {"input_type": "manual"}
            },
            "file": {
                "label": _("Datei"),
                "type": "file",
                "required": False,
                "depends_on": {"input_type": "file"}
            },
            "show_calculations": {
                "label": _("Rechenweg anzeigen"),
                "type": "checkbox",
                "required": False
            }
        }

    def execute_tool(self, input_params: dict) -> bool:
        try:
            input_type = input_params.get("input_type", "manual")
            show_calculations = "show_calculations" in input_params and input_params["show_calculations"] is True
            
            # Entscheiden, ob wir Dateigröße oder manuelle Eingabe verwenden
            if input_type == "file" and "file" in input_params:
                # Datei wurde hochgeladen, Größe auslesen
                file_info = input_params["file"]
                file_path = file_info["file_path"]
                file_size = os.path.getsize(file_path)
                filename = file_info["filename"]
                
                # Automatisch als Bytes-Wert umsetzen
                size = file_size
                unit = "bytes"
                source_description = f"{_('Dateigröße von')}: {filename}"
            else:
                # Manuelle Eingabe verwenden
                size = float(input_params.get("size", 0))
                unit = input_params.get("unit", "bytes")
                source_description = None
            
            # Umrechnung in Bytes
            bytes_value = self._convert_to_bytes(size, unit)
            
            # Umrechnung in andere Einheiten
            result = self._convert_from_bytes(bytes_value)
            
            # Text-Ausgabe erstellen
            self.output = self._create_output(result, size, unit, source_description, show_calculations)
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
    
    def _create_output(self, result, original_size, original_unit, source_description=None, show_calculations=False):
        """Erstellt eine Text-Ausgabe mit den Umrechnungsergebnissen"""
        # Übersetzbare Texte
        msg_original = _("Originalgröße")
        msg_decimal = _("Dezimale Einheiten (SI)")
        msg_binary = _("Binäre Einheiten (IEC)")
        msg_calculation = _("Rechenweg")
        
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
        
        # Multiplikatoren für den Rechenweg
        multipliers = {
            "bytes": 1,
            "kb": 1000,
            "mb": 1000 * 1000,
            "gb": 1000 * 1000 * 1000,
            "tb": 1000 * 1000 * 1000 * 1000,
            "kib": 1024,
            "mib": 1024 * 1024,
            "gib": 1024 * 1024 * 1024,
            "tib": 1024 * 1024 * 1024 * 1024
        }
        
        # Text-Ausgabe erstellen
        if source_description:
            output_text = f"{source_description}\n\n"
        else:
            output_text = f"{msg_original}: {original_size} {unit_names[original_unit]}\n\n"
            
        # Rechenweg anzeigen, falls gewünscht
        if show_calculations:
            output_text += f"**{msg_calculation}**:\n\n"
            
            # Umrechnung in Bytes
            if original_unit != "bytes":
                multiplier = multipliers[original_unit]
                output_text += f"{original_size} {unit_names[original_unit]} → {_('Bytes')}:\n"
                output_text += f"{original_size} × {multiplier:,} = {result['bytes']:,.0f} {_('Bytes')}\n\n"
            
            # Umrechnung von Bytes in dezimale Einheiten
            output_text += f"{_('Umrechnung in dezimale Einheiten')}:\n"
            if original_unit != "kb":
                output_text += f"{result['bytes']:,.0f} {_('Bytes')} ÷ 1,000 = {result['kb']:,.3f} KB\n"
            if original_unit != "mb":
                output_text += f"{result['kb']:,.3f} KB ÷ 1,000 = {result['mb']:,.3f} MB\n"
            if original_unit != "gb":
                output_text += f"{result['mb']:,.3f} MB ÷ 1,000 = {result['gb']:,.3f} GB\n"
            if original_unit != "tb":
                output_text += f"{result['gb']:,.3f} GB ÷ 1,000 = {result['tb']:,.3f} TB\n\n"
            
            # Umrechnung von Bytes in binäre Einheiten
            output_text += f"{_('Umrechnung in binäre Einheiten')}:\n"
            if original_unit != "kib":
                output_text += f"{result['bytes']:,.0f} {_('Bytes')} ÷ 1,024 = {result['kib']:,.3f} KiB\n"
            if original_unit != "mib":
                output_text += f"{result['kib']:,.3f} KiB ÷ 1,024 = {result['mib']:,.3f} MiB\n"
            if original_unit != "gib":
                output_text += f"{result['mib']:,.3f} MiB ÷ 1,024 = {result['gib']:,.3f} GiB\n"
            if original_unit != "tib":
                output_text += f"{result['gib']:,.3f} GiB ÷ 1,024 = {result['tib']:,.3f} TiB\n\n"
        
        # Ergebnistabellen anzeigen
        output_text += f"**{msg_decimal}**\n"
        output_text += f"- Bytes: {result['bytes']:,.0f} ({descriptions['bytes']})\n"
        output_text += f"- KB: {result['kb']:,.3f} ({descriptions['kb']})\n"
        output_text += f"- MB: {result['mb']:,.3f} ({descriptions['mb']})\n"
        output_text += f"- GB: {result['gb']:,.3f} ({descriptions['gb']})\n"
        output_text += f"- TB: {result['tb']:,.3f} ({descriptions['tb']})\n\n"
        
        output_text += f"**{msg_binary}**\n"
        output_text += f"- KiB: {result['kib']:,.3f} ({descriptions['kib']})\n"
        output_text += f"- MiB: {result['mib']:,.3f} ({descriptions['mib']})\n"
        output_text += f"- GiB: {result['gib']:,.3f} ({descriptions['gib']})\n"
        output_text += f"- TiB: {result['tib']:,.3f} ({descriptions['tib']})\n"
        
        return output_text