// Upload- und Konvertierungsfortschritt überwachen
class UploadProgress {
    constructor() {
        this.form = document.getElementById('toolForm');
        this.fileInput = document.getElementById('file');
        this.progressContainer = document.getElementById('progressContainer');
        this.progressBar = document.querySelector('.progress-bar');
        this.submitButton = document.getElementById('submitButton');
        this.progressText = document.getElementById('progressText');

        this.init();
    }

    init() {
        if (!this.form) return;

        this.form.addEventListener('submit', (e) => {
            // Prüfen, ob eine Datei ausgewählt wurde
            if (this.fileInput.files.length === 0) return;

            e.preventDefault();
            this.startUpload();
        });
    }

    startUpload() {
        // Progress-Container anzeigen und Submit-Button deaktivieren
        this.progressContainer.style.display = 'block';
        this.submitButton.disabled = true;

        // FormData-Objekt für den Upload erstellen
        const formData = new FormData(this.form);

        // XMLHttpRequest für den Upload erstellen
        const xhr = new XMLHttpRequest();

        // Upload-Fortschritt überwachen
        xhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable) {
                const percentComplete = Math.round((e.loaded / e.total) * 100);
                this.updateProgress(percentComplete, 'Upload: ');
            }
        });

        // Upload abgeschlossen
        xhr.addEventListener('load', () => {
            if (xhr.status === 200) {
                // Upload war erfolgreich, jetzt simulieren wir den Konvertierungsfortschritt
                this.simulateConversion();

                // Antwort vom Server anzeigen
                document.querySelector('.container').innerHTML = xhr.responseText;
            } else {
                // Fehler beim Upload
                this.updateProgress(100, 'Fehler beim Upload: ');
                alert('Fehler beim Upload: ' + xhr.statusText);
                this.submitButton.disabled = false;
            }
        });

        // Fehler beim Upload
        xhr.addEventListener('error', () => {
            this.updateProgress(0, 'Fehler: ');
            alert('Fehler beim Upload. Bitte versuchen Sie es erneut.');
            this.submitButton.disabled = false;
        });

        // Upload starten
        xhr.open('POST', this.form.action);
        xhr.send(formData);
    }

    // Fortschrittsanzeige aktualisieren
    updateProgress(percent, prefix = '') {
        this.progressBar.style.width = percent + '%';
        this.progressBar.setAttribute('aria-valuenow', percent);
        if (this.progressText) {
            this.progressText.textContent = prefix + percent + '%';
        }
    }

    // Konvertierungsfortschritt simulieren (da wir keinen Echtzeit-Feedback vom Server bekommen)
    simulateConversion() {
        let progress = 0;
        const interval = setInterval(() => {
            progress += 1;
            if (progress <= 90) {
                this.updateProgress(progress, 'Konvertierung: ');
            } else {
                clearInterval(interval);
            }
        }, 200);
    }
}

// Initialisierung, sobald das DOM geladen ist
document.addEventListener('DOMContentLoaded', () => {
    new UploadProgress();
});