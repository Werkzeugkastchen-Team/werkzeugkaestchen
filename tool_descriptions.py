# tool_descriptions.py
# This file contains descriptions for all tools in the application

TOOL_DESCRIPTIONS = {
    "Base64EncodeTool": {
        "description": "Konvertiert Text oder Dateien in das Base64-Format. Ideal für die sichere Übertragung von Binärdaten in textbasierten Systemen wie E-Mail oder HTTP.",
        "use_cases": ["Einbettung von Bildern in HTML/CSS", "Codierung binärer Daten für API-Übertragungen", "Sichere Übermittlung von Zeichen, die in URLs problematisch sein können"]
    },
    "Base64DecodeTool": {
        "description": "Decodiert Base64-kodierte Daten zurück in ihre ursprüngliche Form (Text oder Binärdaten). Nützlich zum Entschlüsseln von Base64-Inhalten.",
        "use_cases": ["Extraktion von Daten aus API-Antworten", "Wiederherstellen von Binärdateien aus Base64-Text", "Analyse kodierter Inhalte"]
    },
    "FileSizeCalculatorTool": {
        "description": "Berechnet die Größe von Dateien in verschiedenen Einheiten (Bytes, KB, MB, GB). Hilft bei der Einschätzung von Speicheranforderungen.",
        "use_cases": ["Überprüfung von Upload-Größen", "Planung von Speicherkapazitäten", "Optimierung von Dateien für Web-Anwendungen"]
    },
    "QrCodeGeneratorTool": {
        "description": "Erstellt QR-Codes aus Text, URLs oder anderen Daten. Ideal für kontaktlose Informationsübermittlung und schnellen Datenzugriff über mobile Geräte.",
        "use_cases": ["Erstellung von Kontaktinformationen zum Scannen", "Generierung von Website-Links für Print-Materialien", "Entwicklung von kontaktlosen Zahlungslösungen"]
    },
    "NumberConverterTool": {
        "description": "Konvertiert Zahlen zwischen verschiedenen Zahlensystemen (Dezimal, Binär, Hexadezimal, Oktal). Unverzichtbar für Programmierer und IT-Spezialisten.",
        "use_cases": ["Umrechnung für Programmieraufgaben", "Analyse von Speicheradressen", "Arbeit mit Farbcodes und anderen hexadezimalen Werten"]
    },
    "ImageConverterTool": {
        "description": "Wandelt Bilder zwischen verschiedenen Formaten um (JPG, PNG, WebP, etc.) und ermöglicht die Anpassung von Qualität und Größe.",
        "use_cases": ["Optimierung von Bildern für Websites", "Anpassung an spezifische Formatanforderungen", "Konvertierung für bessere Kompatibilität"]
    },
    "WordCounterTool": {
        "description": "Zählt Wörter, Zeichen und Absätze in einem Text. Perfekt für Autoren, SEO-Experten und Content-Ersteller zur Analyse von Textinhalten.",
        "use_cases": ["Überprüfung von Texten auf Längenanforderungen", "Analyse von Dokumenten", "Optimierung von SEO-Content"]
    },
    "PasswordGeneratorTool": {
        "description": "Erstellt sichere, zufällige Passwörter mit anpassbarer Länge und Zeichensatz-Optionen. Erhöht die Sicherheit Ihrer Online-Konten.",
        "use_cases": ["Generierung sicherer Zugangsdaten", "Erstellung von API-Schlüsseln", "Verbesserung der Kontosicherheit"]
    },
    "CalendarWeekTool": {
        "description": "Berechnet Kalenderwochen für beliebige Daten nach ISO-8601 Standard. Hilfreich für Projektplanung und Terminkoordination.",
        "use_cases": ["Planung nach Kalenderwochen", "Berechnung von Projektzeitleisten", "Analyse von saisonalen Trends"]
    },
    "ImageCropperTool": {
        "description": "Ermöglicht präzises Zuschneiden von Bildern durch Auswahl des gewünschten Bereichs. Ideal für Profilbilder oder fokussierte Bildausschnitte.",
        "use_cases": ["Anpassung von Bildern für soziale Medien", "Erstellung einheitlicher Produktbilder", "Fokussierung auf relevante Bildbereiche"]
    },
    "RandomNumberGeneratorTool": {
        "description": "Erzeugt Zufallszahlen in einem definierbaren Bereich mit Optionen für Duplikate und Sortierung. Perfekt für Auslosungen und statistische Zwecke.",
        "use_cases": ["Durchführung von Verlosungen", "Erstellung von Test-Datensätzen", "Simulation von Zufallsprozessen"]
    },
    "AudioConverterTool": {
        "description": "Konvertiert Audiodateien zwischen verschiedenen Formaten (MP3, WAV, AAC, FLAC) unter Beibehaltung der Audioqualität.",
        "use_cases": ["Anpassung an Gerätekompatibilität", "Optimierung der Dateigröße", "Vorbereitung von Audio für verschiedene Plattformen"]
    },
    "TextToSpeechTool": {
        "description": "Wandelt geschriebenen Text in natürlich klingende Sprache um. Unterstützt verschiedene Sprachen und Stimmoptionen.",
        "use_cases": ["Erstellung von Audio-Content", "Barrierefreiheit für sehbehinderte Nutzer", "Entwicklung von Sprachassistenten"]
    },
    "UnixTimestampTool": {
        "description": "Konvertiert zwischen menschenlesbaren Datumsformaten und Unix-Zeitstempeln. Essentiell für Entwickler und Systemadministratoren.",
        "use_cases": ["Fehlersuche in Logs", "Zeitberechnung in Anwendungen", "Planung von zeitgesteuerten Aufgaben"]
    },
    "TexteVergleichenTool": {
        "description": "Vergleicht zwei Texte und hebt Unterschiede hervor. Ideal für die Überprüfung von Änderungen in Dokumenten oder Code.",
        "use_cases": ["Vergleich von Vertragsentwürfen", "Identifikation von Änderungen in Texten", "Code-Review und Dokumentenprüfung"]
    },
    "JSONValidierungTool": {
        "description": "Überprüft JSON-Daten auf syntaktische Korrektheit und Validität. Hilfreich für Entwickler bei der Arbeit mit APIs und Datenaustausch.",
        "use_cases": ["Validierung von API-Antworten", "Fehlersuche in JSON-Daten", "Test von Datenstrukturen"]
    },
    "JSONFormatierungTool": {
        "description": "Formatiert JSON-Daten für bessere Lesbarkeit mit Einrückungen und strukturierter Darstellung. Erleichtert die Analyse komplexer Datenstrukturen.",
        "use_cases": ["Übersichtliche Darstellung von API-Antworten", "Vorbereitung von JSON für Dokumentation", "Verbesserung der Lesbarkeit von Konfigurationsdateien"]
    },
    "UnitConverterTool": {
        "description": "Wandelt Werte zwischen verschiedenen Maßeinheiten um (Länge, Gewicht, Temperatur, etc.). Präzise und zuverlässige Konvertierungen für alltägliche und technische Anwendungen.",
        "use_cases": ["Umrechnung für internationale Projekte", "Wissenschaftliche Berechnungen", "Anpassung von Rezepten und Anleitungen"]
    },
    "DateCalculatorTool": {
        "description": "Berechnet Zeiträume zwischen Daten oder addiert/subtrahiert Tage zu einem Datum. Perfekt für Projekt- und Eventplanung.",
        "use_cases": ["Berechnung von Projektlaufzeiten", "Planung von Terminen und Fristen", "Analyse von Zeiträumen"]
    },
    "PlaceholderTextTool": {
        "description": "Generiert Platzhaltertext (Lorem Ipsum) für Design- und Layoutzwecke. Ideal für die Gestaltung von Webseiten, Dokumenten und Präsentationen.",
        "use_cases": ["Vorschau von Webseitenlayouts", "Gestaltung von Druckmaterialien", "Erstellung von Design-Mockups"]
    },
    "ColorConverterTool": {
        "description": "Konvertiert Farben zwischen verschiedenen Formaten (HEX, RGB, HSL) und bietet eine visuelle Vorschau. Unverzichtbar für Designer und Entwickler.",
        "use_cases": ["Anpassung von Farbwerten für CSS", "Erstellung konsistenter Farbpaletten", "Konvertierung zwischen Designtools"]
    },
    "GifVideoConverterTool": {
        "description": "Konvertiert zwischen GIF-Animationen und Videoformaten. Ermöglicht die Optimierung von animierten Inhalten für verschiedene Plattformen.",
        "use_cases": ["Erstellung von GIFs aus Videos für soziale Medien", "Umwandlung von GIFs in Videos für bessere Qualität", "Optimierung von Animationen für Web"]
    },
    "WhisperSubtitleTool": {
        "description": "Generiert automatisch Untertitel für Videos mithilfe von KI-basierter Spracherkennung. Verbessert die Zugänglichkeit und Nutzererfahrung von Videocontent.",
        "use_cases": ["Erstellung barrierefreier Videos", "Übersetzung von Videoinhalten", "Verbesserung der SEO für Videokanäle"]
    },
    "PdfSplitTool": {
        "description": "Teilt PDF-Dokumente in einzelne Seiten oder Abschnitte. Ideal für die Extraktion spezifischer Informationen aus umfangreichen Dokumenten.",
        "use_cases": ["Aufteilung von großen Berichten", "Extraktion relevanter Seiten", "Organisation von Dokumenten nach Themen"]
    },
    "PdfMergeTool": {
        "description": "Kombiniert mehrere PDF-Dateien zu einem einzigen Dokument. Perfekt für die Erstellung umfassender Berichte oder die Zusammenführung verwandter Dokumente.",
        "use_cases": ["Zusammenstellung von Unterlagen", "Erstellung von Handbüchern aus Einzeldokumenten", "Organisation von digitalem Papierkram"]
    }
}

def get_description(tool_name):
    """Returns the description for a given tool name"""
    tool_info = TOOL_DESCRIPTIONS.get(tool_name, {})
    return tool_info.get("description", "Keine Beschreibung verfügbar.")

def get_use_cases(tool_name):
    """Returns the use cases for a given tool name"""
    tool_info = TOOL_DESCRIPTIONS.get(tool_name, {})
    return tool_info.get("use_cases", [])