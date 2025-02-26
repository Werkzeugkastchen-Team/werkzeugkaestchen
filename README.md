Werkzeugkästchen

Projektstruktur ist noch in Entwicklung?

## Setup

Dies wurde mit **Python 3.10** getestet

- venv erstellen (python 3.10)

```sh
python3 -m venv venv
```

- venv aktivieren

Windows:
```sh
venv\Scripts\activate
```

MacOS/Linux:
```sh
source venv/bin/activate
```

- Abhängigkeiten installieren

```sh
pip install -r requirements.txt
```


## Server starten

```sh
flask --app webapp run
```

(`webapp.py` ist die Hauptklasse)

## Development Environment

Am Besten funktioniert VSCode mit den Python Extensions
