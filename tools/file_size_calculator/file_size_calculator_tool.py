from tool_interface import MiniTool, OutputType
import os


class FileSizeCalculatorTool(MiniTool):
    def __init__(self):
        super().__init__("Dateigrößenberechner", "FileSizeCalculatorTool")
        self.description = "Berechnet die Dateigröße in verschiedenen Einheiten (MB, MiB, usw.)"
        self.input_params = {
            "file": "file"
        }

    def execute_tool(self, input_params: dict) -> bool:
        try:
            # Get the file info from input parameters
            file_data = input_params.get("file", None)

            if not file_data:
                self.error_message = "Keine Datei hochgeladen"
                return False

            # Get the file path and name
            file_path = file_data["file_path"]
            file_name = file_data["filename"]

            # Get file size in bytes
            file_size_bytes = os.path.getsize(file_path)

            # Calculate size in different units
            # Decimal units (powers of 10)
            kb = file_size_bytes / 1000
            mb = kb / 1000
            gb = mb / 1000

            # Binary units (powers of 2)
            kib = file_size_bytes / 1024
            mib = kib / 1024
            gib = mib / 1024

            # Format the output as HTML with better styling
            result = f"""
            <div class="file-size-results">
                <h4>Datei: <span class="text-primary">{file_name}</span></h4>
                <p>Gesamtgröße: <strong>{file_size_bytes:,}</strong> Bytes</p>
                
                <div class="row mt-4">
                    <div class="col-md-6">
                        <div class="card mb-4">
                            <div class="card-header bg-primary text-white">
                                <h5 class="mb-0">Dezimale Einheiten (SI)</h5>
                            </div>
                            <div class="card-body">
                                <table class="table table-striped">
                                    <thead>
                                        <tr>
                                            <th>Einheit</th>
                                            <th>Wert</th>
                                            <th>Beschreibung</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>Bytes</td>
                                            <td>{file_size_bytes:,}</td>
                                            <td>Bytes</td>
                                        </tr>
                                        <tr>
                                            <td>KB</td>
                                            <td>{kb:.2f}</td>
                                            <td>Kilobyte (1000 Bytes)</td>
                                        </tr>
                                        <tr>
                                            <td>MB</td>
                                            <td>{mb:.2f}</td>
                                            <td>Megabyte (1000 KB)</td>
                                        </tr>
                                        <tr>
                                            <td>GB</td>
                                            <td>{gb:.2f}</td>
                                            <td>Gigabyte (1000 MB)</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                    
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header bg-info text-white">
                                <h5 class="mb-0">Binäre Einheiten (IEC)</h5>
                            </div>
                            <div class="card-body">
                                <table class="table table-striped">
                                    <thead>
                                        <tr>
                                            <th>Einheit</th>
                                            <th>Wert</th>
                                            <th>Beschreibung</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>Bytes</td>
                                            <td>{file_size_bytes:,}</td>
                                            <td>Bytes</td>
                                        </tr>
                                        <tr>
                                            <td>KiB</td>
                                            <td>{kib:.2f}</td>
                                            <td>Kibibyte (1024 Bytes)</td>
                                        </tr>
                                        <tr>
                                            <td>MiB</td>
                                            <td>{mib:.2f}</td>
                                            <td>Mebibyte (1024 KiB)</td>
                                        </tr>
                                        <tr>
                                            <td>GiB</td>
                                            <td>{gib:.2f}</td>
                                            <td>Gibibyte (1024 MiB)</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """

            self.output = result
            return True

        except Exception as e:
            self.error_message = f"Fehler bei der Berechnung der Dateigröße: {str(e)}"
            return False
