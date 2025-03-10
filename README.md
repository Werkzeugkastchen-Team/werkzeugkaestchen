## Setup

Dies wurde mit **Python 3.10** getestet

- **venv erstellen (python 3.10)**

```sh
python3 -m venv venv
```

oder

```sh
python -m venv venv
```

- **venv aktivieren**

Windows:
```sh
venv\Scripts\activate
```

MacOS/Linux:
```sh
source venv/bin/activate
```

- **Abhängigkeiten installieren**

```sh
pip install -r requirements.txt
```

>Wenn neue Abhängigkeiten hinzugefügt wurde, muss man das nochmal ausführen.


## Server starten

```sh
flask --app webapp run
```

(`webapp.py` ist die Hauptklasse)

## Development Environment

Am Besten funktioniert VSCode mit den Python Extensions

## PyTest Tests ausführen

Pytest ist in `pytest.ini` so konfiguriert, im `tests/` Ordner alle test_*.py Dateien auszuführen

Um sie manuell auszufüren, im Terminal:

```sh
pytest
```

`pytest -v` für mehr Details.
