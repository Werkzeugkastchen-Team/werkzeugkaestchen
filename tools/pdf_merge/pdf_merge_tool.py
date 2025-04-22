import os
import tempfile
import base64
from tool_interface import MiniTool
from PyPDF2 import PdfMerger


class PdfMergeTool(MiniTool):
    def __init__(self):
        super().__init__("PDF Merge Tool", "PdfMergeTool")
        self.description = "Fügt mehrere PDF-Dateien zu einer einzigen Datei zusammen"
        self.input_params = {
            "pdf_files": "file[]"  # List of PDF files
        }

    def execute_tool(self, input_params: dict) -> bool:
        try:
            pdf_files_info = input_params.get("pdf_files", [])

            # Normalize to a list
            if isinstance(pdf_files_info, dict):
                pdf_files_info = [pdf_files_info]

            pdf_order_str = input_params.get("pdf_order", "")

            # Validate input files
            if not pdf_files_info or len(pdf_files_info) < 2:
                self.error_message = "Bitte laden Sie mindestens zwei gültige PDF-Dateien hoch."
                return False


            # Validate ordering
            if not pdf_order_str:
                self.error_message = "Keine Reihenfolge der PDFs angegeben."
                return False

            ordered_filenames = [name.strip() for name in pdf_order_str.split(",")]

            # Create a lookup dict for the uploaded files
            file_dict = {f['filename']: f for f in pdf_files_info}

            # Match files in user-specified order
            ordered_files = []
            for name in ordered_filenames:
                file_info = file_dict.get(name)
                if not file_info:
                    self.error_message = f"Datei '{name}' nicht gefunden oder nicht hochgeladen."
                    return False
                ordered_files.append(file_info)

            # Begin merging
            merger = PdfMerger()
            filenames = []

            for file_info in ordered_files:
                file_path = file_info.get("file_path")
                filename = file_info.get("filename")

                if not file_path or not filename.lower().endswith(".pdf"):
                    self.error_message = "Eine oder mehrere Dateien sind ungültig oder nicht im PDF-Format."
                    return False

                merger.append(file_path)
                filenames.append(filename)

            # Save merged file
            temp_dir = tempfile.gettempdir()
            merged_filename = "zusammengefuegt.pdf"
            merged_path = os.path.join(temp_dir, merged_filename)

            with open(merged_path, 'wb') as f_out:
                merger.write(f_out)
            merger.close()

            base64_pdf = self._get_file_base64(merged_path)

            self.output = f"""
            <div class="pdf-merge-tool">
                <h5>PDF-Dateien erfolgreich zusammengeführt</h5>
                <p>Zusammengeführt in dieser Reihenfolge:</p>
                <ol>
                    {''.join(f"<li>{name}</li>" for name in filenames)}
                </ol>
                <a href="data:application/pdf;base64,{base64_pdf}" download="{merged_filename}" class="btn btn-success mt-3">
                    📄 Zusammengeführte PDF herunterladen
                </a>
            </div>
            """
            return True

        except Exception as e:
            self.error_message = f"Fehler beim Zusammenführen: {str(e)}"
            return False


    def _get_file_base64(self, file_path):
        with open(file_path, "rb") as file:
            return base64.b64encode(file.read()).decode("utf-8")
