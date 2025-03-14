# FFmpeg Installation Guide

FFmpeg ist eine erforderliche Abhängigkeit für den Audio-Konverter. Dieses Dokument enthält Anweisungen zur Installation von FFmpeg auf verschiedenen Betriebssystemen.

## Voraussetzungen

- Python 3.x
- pip (Python Package Manager)

## Python-Pakete installieren

Nach der Installation von FFmpeg müssen Sie die erforderlichen Python-Pakete installieren:

```bash
pip install ffmpeg-python pydub
```

## FFmpeg Installation

### Windows

#### Option 1: Manuelle Installation
1. Besuchen Sie die offizielle FFmpeg-Website: https://ffmpeg.org/download.html
2. Laden Sie die Windows-Version herunter
3. Extrahieren Sie die Dateien
4. Fügen Sie den Pfad zum FFmpeg-Binärverzeichnis zu Ihren Umgebungsvariablen hinzu

#### Option 2: Installation über Chocolatey
```powershell
choco install ffmpeg
```

### macOS

#### Installation über Homebrew
```bash
brew install ffmpeg
```

### Linux

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

#### Fedora
```bash
sudo dnf install ffmpeg
```

## Überprüfung der Installation

Um zu überprüfen, ob FFmpeg korrekt installiert wurde, öffnen Sie eine Kommandozeile und geben Sie ein:

```bash
ffmpeg -version
```

Sie sollten die FFmpeg-Versionsinformationen sehen. Wenn Sie eine Fehlermeldung wie "ffmpeg is not recognized" erhalten:

1. Stellen Sie sicher, dass FFmpeg installiert ist
2. Überprüfen Sie, ob der FFmpeg-Pfad in Ihren Umgebungsvariablen korrekt gesetzt ist
3. Starten Sie Ihre Python-Umgebung neu

## Fehlerbehebung

### Windows
- Wenn FFmpeg nicht erkannt wird, überprüfen Sie die Umgebungsvariablen:
  1. Öffnen Sie die Systemsteuerung
  2. System und Sicherheit > System
  3. Erweiterte Systemeinstellungen
  4. Umgebungsvariablen
  5. Fügen Sie den Pfad zum FFmpeg-Binärverzeichnis zur PATH-Variable hinzu

### macOS/Linux
- Wenn der Befehl `ffmpeg` nicht gefunden wird, überprüfen Sie die Installation:
  ```bash
  which ffmpeg
  ```
- Falls nicht gefunden, stellen Sie sicher, dass die Installation erfolgreich war und der Pfad korrekt ist

## Support

Bei Problemen mit der Installation:
1. Überprüfen Sie die FFmpeg-Dokumentation: https://ffmpeg.org/documentation.html
2. Stellen Sie sicher, dass alle Abhängigkeiten installiert sind
3. Kontaktieren Sie den Support bei weiteren Fragen 