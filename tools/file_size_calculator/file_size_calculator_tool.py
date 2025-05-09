from tool_interface import MiniTool, OutputType
import os
from flask_babel import lazy_gettext as _


class FileSizeCalculatorTool(MiniTool):
    def __init__(self):
        # Übersetzungsvariablen
        tool_title = _("Dateigrößenberechner")
        tool_desc = _(
            "Berechnet die Dateigröße in verschiedenen Einheiten (MB, MiB, usw.)")
        super().__init__(tool_title, "FileSizeCalculatorTool")
        self.description = tool_desc
        self.input_params = {
            "file": "file"
        }

    def execute_tool(self, input_params: dict) -> bool:
        try:
            file_data = input_params.get("file", None)
            if not file_data:
                self.error_message = _("Keine Datei hochgeladen")
                return False

            file_path = file_data["file_path"]
            file_name = file_data["filename"]
            file_size_bytes = os.path.getsize(file_path)

            # Berechnungen mit höherer Präzision
            kb = file_size_bytes / 1000
            mb = kb / 1000
            gb = mb / 1000
            kib = file_size_bytes / 1024
            mib = kib / 1024
            gib = mib / 1024

            # Übersetzbare Texte in Variablen
            msg_date = _("Datei")
            msg_file_size = _("Gesamtgröße")
            msg_bytes = _("Bytes")
            msg_decimal = _("Dezimale Einheiten (SI)")
            msg_binary = _("Binäre Einheiten (IEC)")
            msg_unit = _("Einheit")
            msg_value = _("Wert")
            msg_description = _("Beschreibung")
            msg_kilobyte = _("Kilobyte (1000 Bytes)")
            msg_megabyte = _("Megabyte (1000 KB)")
            msg_gigabyte = _("Gigabyte (1000 MB)")
            msg_kibibyte = _("Kibibyte (1024 Bytes)")
            msg_mebibyte = _("Mebibyte (1024 KiB)")
            msg_gibibyte = _("Gibibyte (1024 MiB)")

            # Formatierungsfunktion für die Werte
            def format_size(size):
                if size >= 0.01:
                    return f"{size:.2f}"
                elif size >= 0.00001:
                    # Für sehr kleine Werte mehr Dezimalstellen anzeigen
                    return f"{size:.6f}"
                else:
                    # Für extrem kleine Werte normale Dezimalzahlen verwenden
                    return f"{size:.9f}"

            # Zusammenbau des HTML-Strings mit den Variablen
            result = (
                "<div class=\"file-size-results\">"
                f"<h4>{msg_date}: <span class=\"text-primary\">{file_name}</span></h4>"
                f"<p>{msg_file_size}: <strong>{file_size_bytes:,}</strong> {msg_bytes}</p>"

                "<div class=\"row mt-4\">"
                "<div class=\"col-md-6\">"
                "<div class=\"card mb-4\">"
                f"<div class=\"card-header bg-primary text-white\">"
                f"<h5 class=\"mb-0\">{msg_decimal}</h5>"
                "</div>"
                "<div class=\"card-body\">"
                "<table class=\"table table-striped\">"
                "<thead>"
                "<tr>"
                f"<th>{msg_unit}</th>"
                f"<th>{msg_value}</th>"
                f"<th>{msg_description}</th>"
                "</tr>"
                "</thead>"
                "<tbody>"
                "<tr>"
                f"<td>{msg_bytes}</td>"
                f"<td>{file_size_bytes:,}</td>"
                f"<td>{msg_bytes}</td>"
                "</tr>"
                "<tr>"
                "<td>KB</td>"
                f"<td>{format_size(kb)}</td>"
                f"<td>{msg_kilobyte}</td>"
                "</tr>"
                "<tr>"
                "<td>MB</td>"
                f"<td>{format_size(mb)}</td>"
                f"<td>{msg_megabyte}</td>"
                "</tr>"
                "<tr>"
                "<td>GB</td>"
                f"<td>{format_size(gb)}</td>"
                f"<td>{msg_gigabyte}</td>"
                "</tr>"
                "</tbody>"
                "</table>"
                "</div>"
                "</div>"
                "</div>"

                "<div class=\"col-md-6\">"
                "<div class=\"card\">"
                f"<div class=\"card-header bg-info text-white\">"
                f"<h5 class=\"mb-0\">{msg_binary}</h5>"
                "</div>"
                "<div class=\"card-body\">"
                "<table class=\"table table-striped\">"
                "<thead>"
                "<tr>"
                f"<th>{msg_unit}</th>"
                f"<th>{msg_value}</th>"
                f"<th>{msg_description}</th>"
                "</tr>"
                "</thead>"
                "<tbody>"
                "<tr>"
                f"<td>{msg_bytes}</td>"
                f"<td>{file_size_bytes:,}</td>"
                f"<td>{msg_bytes}</td>"
                "</tr>"
                "<tr>"
                "<td>KiB</td>"
                f"<td>{format_size(kib)}</td>"
                f"<td>{msg_kibibyte}</td>"
                "</tr>"
                "<tr>"
                "<td>MiB</td>"
                f"<td>{format_size(mib)}</td>"
                f"<td>{msg_mebibyte}</td>"
                "</tr>"
                "<tr>"
                "<td>GiB</td>"
                f"<td>{format_size(gib)}</td>"
                f"<td>{msg_gibibyte}</td>"
                "</tr>"
                "</tbody>"
                "</table>"
                "</div>"
                "</div>"
                "</div>"
                "</div>"
                "</div>"
            )

            self.output = result
            return True

        except Exception as e:
            self.error_message = _(
                "Fehler bei der Berechnung der Dateigröße:") + " " + str(e)
            return False
