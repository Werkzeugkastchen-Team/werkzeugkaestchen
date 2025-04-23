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

>Wenn neue Abhängigkeiten hinzugefügt wurden, muss man das nochmal ausführen.

>Wegen des TTS Tools wird PyTorch mit heruntergeladen und kann bis zu 4GB groß sein!


## Server starten

```sh
flask --app webapp run
```

(`webapp.py` ist die Hauptklasse)

## Ollama aufsetzen (für Texte zusammenfassen Tool)

Dies ist ein Docker Container der im Hintergrund ausgeführt werden muss, damit das Tool funktioniert.

Linux und MacOS:
```sh
sudo docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama && docker exec -it ollama ollama run gemma3:1b
```

Windows:
```sh
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

```sh
docker exec -it ollama ollama run gemma3:1b
```

Und noch zusätzlich für gemma3:4b:

```sh
docker exec -it ollama ollama run gemma3:4b
```

Wenn man die Modelle ändern will, dann muss man das Tool und den ollama run Befehl anpassen.

>Gemma 3 1B ist sehr leicht (~1GB), ist aber eher schlecht.

>Gemma 3 4B ist etwas schwerer (~4GB), ist aber besser als 1B. Auf unseren halbwegs aktuellen Laptops sollten beide recht OK laufen.

## Development Environment

Am Besten funktioniert VSCode mit den Python Extensions

## PyTest Tests ausführen

Pytest ist in `pytest.ini` so konfiguriert, im `tests/` Ordner alle test_*.py Dateien auszuführen

Um sie manuell auszufüren, im Terminal:

```sh
pytest
```

`pytest -v` für mehr Details.

# Troubleshooting

Wenn man keine KI-Tools wie TTS Verwenden will, folende Einträge in requirements.txt entfernen:

```
torch
torchaudio
coqui-tts
```