# passswordmanager
password manger in python
# 🔐 Lokaler Passwortmanager (Python + GUI)

Ein einfacher, lokaler Passwortmanager mit grafischer Benutzeroberfläche, entwickelt in Python. Der Passwortmanager speichert Passwörter sicher lokal auf dem System – ideal für den privaten Gebrauch ohne Cloud-Abhängigkeit.

## 🧠 Features

- Lokale Speicherung von Passwörtern in verschlüsselter Datei
- Benutzerfreundliche GUI mit Tkinter
- Hinzufügen, Anzeigen und Löschen von Einträgen
- Sichere Verschlüsselung mit Fernet (Symmetrische Verschlüsselung)
- Passwort-Generator (optional)

## 🛠 Voraussetzungen

- Python 3.8 oder höher
- Abhängigkeiten:
  - `tkinter`
  - `cryptography`

Installation der benötigten Pakete (sofern nicht vorhanden):

```bash
pip install cryptography
tkinter ist bei den meisten Python-Installationen bereits enthalten. Falls nicht, installiere es manuell je nach Betriebssystem.

▶️ Nutzung
Klone das Repository oder lade die Dateien herunter:

bash
Kopieren
Bearbeiten
git clone https://github.com/dein-nutzername/passwortmanager.git
cd passwortmanager
Starte die Anwendung:

bash
Kopieren
Bearbeiten
python passwortmanager.py
Lege beim ersten Start ein Master-Passwort fest. Dieses schützt deine gespeicherten Daten.

Bediene den Manager über die intuitive Benutzeroberfläche.

🗃 Dateistruktur
graphql
Kopieren
Bearbeiten
passwortmanager/
├── passwortmanager.py     # Hauptdatei mit GUI und Logik
├── data.enc               # Verschlüsselte Passwortdatenbank (wird automatisch erstellt)
└── README.md              # Diese Datei
🔒 Sicherheitshinweis
Alle Passwörter werden verschlüsselt gespeichert (z.B. mit Fernet AES-256).

Das Master-Passwort wird nicht gespeichert – vergiss es nicht!

Die Datei data.enc enthält deine verschlüsselten Daten. Halte sie sicher!

🚧 Geplante Funktionen
Unterstützung mehrerer Benutzer

Automatischer Passwort-Generator

Backup/Restore-Funktion

Dark Mode GUI

👨‍💻 Autor
Albert Heruth
Auszubildender Fachinformatiker für Systemintegration
GitHub: @hackbert301009
