import os
import tempfile
import base64
from tool_interface import MiniTool
from PyPDF2 import PdfReader, PdfWriter


class PdfSplitTool(MiniTool):
    def __init__(self):
        super().__init__("PDF Split Tool", "PdfSplitTool")
        self.description = "Teilt PDF-Dateien an einer gewählten Seitenzahl"
        self.input_params = {
            "pdf_file": "file",
            "split_page": "string"  # Page number to split at (first page of second part)
        }

    def execute_tool(self, input_params: dict) -> bool:
        try:
            # Get parameters
            pdf_file_info = input_params.get("pdf_file", None)
            split_page_str = input_params.get("split_page", "")

            # Validate inputs
            if not pdf_file_info:
                self.error_message = "Bitte wählen Sie eine PDF-Datei aus"
                return False

            if not split_page_str:
                self.error_message = "Bitte geben Sie eine Seitenzahl an"
                return False

            try:
                split_page = int(split_page_str)
                if split_page < 2:
                    self.error_message = "Die Seitenzahl muss mindestens 2 sein"
                    return False
            except ValueError:
                self.error_message = "Bitte geben Sie eine gültige Seitenzahl ein"
                return False

            # Get file path
            file_path = pdf_file_info["file_path"]
            filename = pdf_file_info["filename"]
            filename_base = os.path.splitext(filename)[0]

            # Open the PDF file
            with open(file_path, 'rb') as file:
                pdf = PdfReader(file)
                total_pages = len(pdf.pages)

                if split_page > total_pages:
                    self.error_message = f"Die Seitenzahl muss kleiner sein als die Gesamtseitenzahl ({total_pages})"
                    return False

                # Create writers for the two parts
                part1_writer = PdfWriter()
                part2_writer = PdfWriter()

                # Add pages to the first part (pages 0 to split_page-1)
                for page_num in range(0, split_page - 1):
                    part1_writer.add_page(pdf.pages[page_num])

                # Add pages to the second part (pages split_page-1 to end)
                for page_num in range(split_page - 1, total_pages):
                    part2_writer.add_page(pdf.pages[page_num])

                # Save the split PDFs to temporary files
                temp_dir = tempfile.gettempdir()
                part1_filename = f"{filename_base}_teil1.pdf"
                part2_filename = f"{filename_base}_teil2.pdf"
                part1_path = os.path.join(temp_dir, part1_filename)
                part2_path = os.path.join(temp_dir, part2_filename)

                with open(part1_path, 'wb') as output_file:
                    part1_writer.write(output_file)

                with open(part2_path, 'wb') as output_file:
                    part2_writer.write(output_file)

                # Convert the PDFs to base64 for download links
                part1_base64 = self._get_file_base64(part1_path)
                part2_base64 = self._get_file_base64(part2_path)

            # Create HTML output with download links
            result = f"""
            <div class="pdf-split-result">
                <div class="row">
                    <div class="col-md-12">
                        <div class="card">
                            <div class="card-header bg-success text-white">
                                <h5 class="mb-0">PDF erfolgreich geteilt</h5>
                            </div>
                            <div class="card-body">
                                <div class="alert alert-info">
                                    <p>Die PDF-Datei <strong>{filename}</strong> wurde erfolgreich bei Seite {split_page} geteilt.</p>
                                    <p>Gesamtseitenzahl: {total_pages}</p>
                                    <ul>
                                        <li>Teil 1: Seiten 1 bis {split_page - 1}</li>
                                        <li>Teil 2: Seiten {split_page} bis {total_pages}</li>
                                    </ul>
                                </div>
                                
                                <div class="row mt-4">
                                    <div class="col-md-6 text-center">
                                        <div class="card">
                                            <div class="card-header bg-primary text-white">
                                                Teil 1 ({split_page - 1} Seiten)
                                            </div>
                                            <div class="card-body">
                                                <p class="mb-2">Enthält Seiten 1 bis {split_page - 1}</p>
                                                <a href="data:application/pdf;base64,{part1_base64}" 
                                                   download="{part1_filename}" 
                                                   class="btn btn-primary">
                                                   <i class="fas fa-download"></i> Teil 1 herunterladen
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6 text-center">
                                        <div class="card">
                                            <div class="card-header bg-primary text-white">
                                                Teil 2 ({total_pages - split_page + 1} Seiten)
                                            </div>
                                            <div class="card-body">
                                                <p class="mb-2">Enthält Seiten {split_page} bis {total_pages}</p>
                                                <a href="data:application/pdf;base64,{part2_base64}" 
                                                   download="{part2_filename}" 
                                                   class="btn btn-primary">
                                                   <i class="fas fa-download"></i> Teil 2 herunterladen
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """

            self.output = result
            return True

        except Exception as e:
            self.error_message = f"Fehler beim Teilen der PDF-Datei: {str(e)}"
            return False

    def _get_file_base64(self, file_path):
        """Convert file to base64 string for embedding in HTML"""
        with open(file_path, "rb") as file:
            return base64.b64encode(file.read()).decode("utf-8")