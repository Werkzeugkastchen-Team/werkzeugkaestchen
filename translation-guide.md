# Mehrsprachigkeit im Werkzeugkästchen-Projekt

Diese Anleitung beschreibt, wie du mit dem Übersetzungssystem (i18n) im Werkzeugkästchen-Projekt arbeiten kannst.

## Überblick

Das Projekt verwendet Flask-Babel für die Internationalisierung. Aktuell werden zwei Sprachen unterstützt:
- Deutsch (de) - Standardsprache
- Englisch (en)

## Texte für die Übersetzung markieren

### In HTML/Jinja-Templates

Umschließe alle sichtbaren Texte mit der `_()` Funktion:

```html
<!-- Statt: -->
<h1>Werkzeugkästchen</h1>

<!-- Schreibe: -->
<h1>{{ _('Werkzeugkästchen') }}</h1>
```

Bei Attributen:

```html
<input placeholder="{{ _('Suchbegriff eingeben...') }}">
```

### In Python-Code

Importiere die `gettext`-Funktion und verwende sie für alle Texte:

```python
from flask_babel import gettext as _

# Statt:
error_message = "Diese Datei ist zu groß."

# Schreibe:
error_message = _("Diese Datei ist zu groß.")
```

## Workflow für Übersetzungen

### 1. Texte extrahieren

Nachdem du neue zu übersetzende Texte markiert hast, musst du sie extrahieren:

```bash
pybabel extract -F babel.cfg -o messages.pot .
```

### 2. Übersetzungsdateien aktualisieren

Wenn du zum ersten Mal Übersetzungsdateien erstellst:

```bash 
pybabel init -i messages.pot -d translations -l de
pybabel init -i messages.pot -d translations -l en
```

Wenn du bereits Übersetzungsdateien hast und nur neue Texte hinzufügst:

```bash
pybabel update -i messages.pot -d translations
```

### 3. Übersetzungen eintragen

Öffne die Übersetzungsdateien mit einem Texteditor:

- `translations/de/LC_MESSAGES/messages.po` (Deutsch)
- `translations/en/LC_MESSAGES/messages.po` (Englisch)

Für jeden Text findest du einen Eintrag wie diesen:

```
#: templates/index.jinja:5
msgid "Werkzeugkästchen"
msgstr ""
```

Füge die Übersetzung in `msgstr` ein:

```
#: templates/index.jinja:5
msgid "Werkzeugkästchen"
msgstr "Toolbox"  # <- Hier die englische Übersetzung eintragen
```

### 4. Übersetzungen kompilieren

Nach dem Eintragen der Übersetzungen musst du sie kompilieren:

```bash
pybabel compile -d translations
```

## Testen der Übersetzungen

Um zu testen, ob deine Übersetzungen funktionieren:

1. Starte die Flask-App
2. Wechsle zwischen den Sprachen, indem du `?language=de` oder `?language=en` an die URL anhängst oder den Sprachumschalter in der Navigation verwendest

## Häufige Probleme und Lösungen

### Problem: Änderungen werden nicht angezeigt

- Stelle sicher, dass du die Übersetzungen kompiliert hast (`pybabel compile`)
- Leere den Browser-Cache oder starte die Flask-App neu

### Problem: Texte werden nicht extrahiert

- Überprüfe, ob du die korrekte Syntax verwendest: `{{ _('Text') }}` in Templates oder `_('Text')` in Python
- Stelle sicher, dass die Dateien im richtigen Format sind und von babel.cfg erfasst werden

### Problem: Flask-Babel findet die Übersetzungen nicht

- Überprüfe die Ordnerstruktur: Es sollte `translations/[Sprachcode]/LC_MESSAGES/messages.po` sein
- Stelle sicher, dass die Einstellung `BABEL_TRANSLATION_DIRECTORIES` korrekt ist

## Tipps

- Verwende für einen Text immer exakt die gleiche deutsche Originalformulierung, sonst werden mehrere Übersetzungseinträge erstellt
- Achte auf Formatierungszeichen und Variablen: `_('Hallo, %(name)s!')` muss auch in der Übersetzung die Variable enthalten

## Wörterbuch der wichtigsten Übersetzungen

| Deutsch | Englisch |
|---------|----------|
| Werkzeugkästchen | Toolbox |
| Über uns | About us |
| Kontakt | Contact |
| Startseite | Home |
| Datenschutz | Privacy Policy |
| Impressum | Imprint |
