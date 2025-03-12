import random
import string
from tool_interface import MiniTool


class PasswordGeneratorTool(MiniTool):
    name = "Passwortgenerator"
    description = "Generiert starke, zufällige Passwörter mit anpassbaren Optionen für Länge und Zeichentypen."

    def __init__(self):
        super().__init__(self.name, "PasswordGeneratorTool")
        self.input_params = {
            "length": "string",
            "include_lowercase": "boolean",
            "include_uppercase": "boolean",
            "include_numbers": "boolean",
            "include_special": "boolean"
        }

    def execute_tool(self, input_params: dict) -> bool:
        try:
            # Get parameters
            try:
                length = int(input_params.get("length", "12"))
            except ValueError:
                self.error_message = "Die Passwortlänge muss eine Zahl sein."
                return False

            if length < 4 or length > 128:
                self.error_message = "Die Passwortlänge muss zwischen 4 und 128 Zeichen liegen."
                return False

            # Explizit prüfen, ob die Schlüssel im Dictionary vorhanden sind
            # Falls nicht, sind die Checkboxen nicht angekreuzt
            include_lowercase = 'include_lowercase' in input_params
            include_uppercase = 'include_uppercase' in input_params
            include_numbers = 'include_numbers' in input_params
            include_special = 'include_special' in input_params

            # Check if at least one character type is selected
            if not any([include_lowercase, include_uppercase, include_numbers, include_special]):
                self.error_message = "Bitte wählen Sie mindestens einen Zeichentyp aus."
                return False

            # Create character pool based on selections
            chars = ""
            if include_lowercase:
                chars += string.ascii_lowercase
            if include_uppercase:
                chars += string.ascii_uppercase
            if include_numbers:
                chars += string.digits
            if include_special:
                chars += "!@#$%^&*()-_=+[]{}|;:,.<>?/"

            # Generate password
            password = ''.join(random.choice(chars) for _ in range(length))

            # Calculate password strength
            strength = self._calculate_strength(
                password, include_lowercase, include_uppercase, include_numbers, include_special)

            # Format the output
            self.output = self._format_output(password, length, strength)
            return True

        except Exception as e:
            self.error_message = f"Fehler bei der Passwortgenerierung: {str(e)}"
            return False

    def _calculate_strength(self, password, has_lower, has_upper, has_numbers, has_special):
        """Calculate the strength of the password based on various factors"""
        score = 0

        # Base score from length
        if len(password) >= 12:
            score += 3
        elif len(password) >= 8:
            score += 2
        else:
            score += 1

        # Add points for character variety
        character_variety = sum(
            [has_lower, has_upper, has_numbers, has_special])
        score += character_variety

        # Categorize strength
        if score >= 6:
            return {"level": "Stark", "color": "success", "description": "Dieses Passwort bietet guten Schutz."}
        elif score >= 4:
            return {"level": "Mittel", "color": "warning", "description": "Dieses Passwort bietet angemessenen Schutz."}
        else:
            return {"level": "Schwach", "color": "danger", "description": "Dieses Passwort könnte stärker sein."}

    def _format_output(self, password, length, strength):
        """Format the output HTML with modern clipboard handling"""
        return f"""
        <div class="card mb-4">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0">Ihr generiertes Passwort</h5>
            </div>
            <div class="card-body">
                <div class="form-group">
                    <label for="password-output">Passwort:</label>
                    <div class="input-group mb-3">
                        <input type="text" class="form-control" id="password-output" value="{password}" readonly>
                        <div class="input-group-append">
                            <button class="btn btn-outline-secondary copy-password-btn" 
                                    data-password="{password}" 
                                    type="button">
                                Kopieren
                            </button>
                        </div>
                    </div>
                </div>
                
                <div class="password-info mt-3">
                    <p><strong>Länge:</strong> {length} Zeichen</p>
                    <p><strong>Stärke:</strong> <span class="badge bg-{strength['color']}">{strength['level']}</span></p>
                    <p>{strength['description']}</p>
                    
                    <div class="mt-3">
                    <a href="/tool/PasswordGeneratorTool" class="btn btn-primary">Neues Passwort generieren</a>                    </div>
                </div>
                
                <div class="alert alert-info mt-3">
                    <strong>Tipp:</strong> Verwenden Sie für jeden Online-Dienst ein einzigartiges Passwort und 
                    erwägen Sie die Nutzung eines Passwort-Managers, um Ihre Passwörter sicher zu verwalten.
                </div>
                
                <script type="text/javascript">
                document.addEventListener('DOMContentLoaded', () => {{
                    // Event delegation for dynamic content [[4]][[8]]
                    document.body.addEventListener('click', (e) => {{
                        if (e.target.matches('.copy-password-btn')) {{
                            const password = e.target.dataset.password;
                            
                            // Modern clipboard API [[5]]
                            navigator.clipboard.writeText(password)
                                .then(() => {{
                                    const btn = e.target;
                                    const originalText = btn.textContent;
                                    
                                    // Update button state
                                    btn.textContent = 'Kopiert!';
                                    btn.classList.replace('btn-outline-secondary', 'btn-success');
                                    
                                    setTimeout(() => {{
                                        btn.textContent = originalText;
                                        btn.classList.replace('btn-success', 'btn-outline-secondary');
                                    }}, 1500);
                                }})
                                .catch(err => {{
                                    console.error('Kopierfehler:', err);
                                    alert('Kopieren fehlgeschlagen. Bitte manuell kopieren.');
                                }});
                        }}
                    }});
                }});
                </script>
            </div>
        </div>
        """
