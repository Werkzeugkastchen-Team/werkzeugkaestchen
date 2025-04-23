import random
import string
from tool_interface import MiniTool
from flask_babel import lazy_gettext as _


class PasswordGeneratorTool(MiniTool):
    name = _("Passwortgenerator")
    description = _("Generiert starke, zufällige Passwörter mit anpassbaren Optionen für Länge und Zeichentypen.")

    def __init__(self):
        super().__init__(self.name, "PasswordGeneratorTool")
        self.info = _(r"Wählen Sie die gewünschte Länge und die zu verwendenden Zeichentypen für Ihr sicheres Passwort aus. Ein starkes Passwort sollte mindestens 12 Zeichen lang sein und verschiedene Zeichentypen enthalten.")
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
                self.error_message = _("Die Passwortlänge muss eine Zahl sein.")
                return False

            if length < 4 or length > 128:
                self.error_message = _("Die Passwortlänge muss zwischen 4 und 128 Zeichen liegen.")
                return False

            # Explizit prüfen, ob die Schlüssel im Dictionary vorhanden sind
            include_lowercase = 'include_lowercase' in input_params
            include_uppercase = 'include_uppercase' in input_params
            include_numbers = 'include_numbers' in input_params
            include_special = 'include_special' in input_params

            # Check if at least one character type is selected
            if not any([include_lowercase, include_uppercase, include_numbers, include_special]):
                self.error_message = _("Bitte wählen Sie mindestens einen Zeichentyp aus.")
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
            error_prefix = _("Fehler bei der Passwortgenerierung:")
            self.error_message = f"{error_prefix} {str(e)}"
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
            return {
                "level": _("Stark"),
                "color": "success",
                "description": _("Dieses Passwort bietet guten Schutz.")
            }
        elif score >= 4:
            return {
                "level": _("Mittel"),
                "color": "warning",
                "description": _("Dieses Passwort bietet angemessenen Schutz.")
            }
        else:
            return {
                "level": _("Schwach"),
                "color": "danger",
                "description": _("Dieses Passwort könnte stärker sein.")
            }

    def _format_output(self, password, length, strength):
        """Format the output HTML with modern clipboard handling"""
        # Escape special characters in the password for safe use in the HTML template
        escaped_password = password.replace("{", "{{").replace("}", "}}").replace("%", "%%")

        # Definieren der übersetzten Strings
        title = _("Ihr generiertes Passwort")
        label_password = _("Passwort:")
        btn_copy = _("Kopieren")
        length_text = _("Länge:")
        characters = _("Zeichen")
        strength_text = _("Stärke:")
        btn_new = _("Neues Passwort generieren")
        tip_title = _("Tipp:")
        tip_text = _("Verwenden Sie für jeden Online-Dienst ein einzigartiges Passwort und erwägen Sie die Nutzung eines Passwort-Managers, um Ihre Passwörter sicher zu verwalten.")
        copied_text = _("Kopiert!")
        copy_error = _("Kopierfehler:")
        copy_failed = _("Kopieren fehlgeschlagen. Bitte manuell kopieren.")

        return f"""
        <div class="card mb-4">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0">{title}</h5>
            </div>
            <div class="card-body">
                <div class="form-group">
                    <label for="password-output">{label_password}</label>
                    <div class="input-group mb-3">
                        <input type="text" class="form-control" id="password-output" value="{escaped_password}" readonly>
                        <div class="input-group-append">
                            <button class="btn btn-outline-secondary copy-password-btn"
                                    data-password="{escaped_password}"
                                    type="button">
                                {btn_copy}
                            </button>
                        </div>
                    </div>
                </div>

                <div class="password-info mt-3">
                    <p><strong>{length_text}</strong> {length} {characters}</p>
                    <p><strong>{strength_text}</strong> <span class="badge bg-{strength['color']}">{strength['level']}</span></p>
                    <p>{strength['description']}</p>

                    <div class="mt-3">
                    <a href="/tool/PasswordGeneratorTool" class="btn btn-primary">{btn_new}</a>
                    </div>
                </div>

                <div class="alert alert-info mt-3">
                    <strong>{tip_title}</strong> {tip_text}
                </div>

                <script type="text/javascript">
                document.addEventListener('DOMContentLoaded', () => {{
                    // Event delegation for dynamic content
                    document.body.addEventListener('click', (e) => {{
                        if (e.target.matches('.copy-password-btn')) {{
                            const password = e.target.dataset.password;

                            // Modern clipboard API
                            navigator.clipboard.writeText(password)
                                .then(() => {{
                                    const btn = e.target;
                                    const originalText = btn.textContent;

                                    // Update button state
                                    btn.textContent = '{copied_text}';
                                    btn.classList.replace('btn-outline-secondary', 'btn-success');

                                    setTimeout(() => {{
                                        btn.textContent = originalText;
                                        btn.classList.replace('btn-success', 'btn-outline-secondary');
                                    }}, 1500);
                                }})
                                .catch(err => {{
                                    console.error('{copy_error}', err);
                                    alert('{copy_failed}');
                                }});
                        }}
                    }});
                }});
                </script>
            </div>
        </div>
        """
