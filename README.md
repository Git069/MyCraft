⚙️ 2. Setup (Klonen & Installation)
Folgen Sie diesen Schritten, um das Projekt lokal einzurichten.

2.1 Repository klonen

Öffnen Sie Ihr Terminal, navigieren Sie zum gewünschten Speicherort und klonen Sie das Repository:

Bash
git clone https://github.com/orgs/github/repositories
cd FrontendTryOutVue
2.2 Backend (Django) einrichten

Das Backend benötigt eine isolierte virtuelle Umgebung (venv_django).

Virtuelle Umgebung erstellen und aktivieren:

Bash
python3 -m venv venv_django
source venv_django/bin/activate
(Ihr Terminal sollte nun (venv_django) anzeigen.)

Abhängigkeiten installieren: Wir installieren alle notwendigen Python-Pakete (Django, DRF, etc.).

Bash
pip install -r requirements.txt
Wichtig: Stellen Sie sicher, dass Sie eine requirements.txt-Datei erstellen, falls Sie dies noch nicht getan haben: pip freeze > requirements.txt. Ihre Kollegen müssen diese Datei dann vor dem Klonen hinzufügen.

Datenbank und Admin einrichten: Führen Sie die Migrationen aus, um die lokale db.sqlite3-Datei zu erstellen (diese ist durch die .gitignore ignoriert).

Bash
python manage.py migrate
python manage.py createsuperuser  # Optional: Erstellt einen Admin-Benutzer
2.3 Frontend (Vue/Vite) einrichten

Das Frontend verwendet Node.js und npm für seine Abhängigkeiten.

In den Frontend-Ordner wechseln:

Bash
cd my-vue-Tryoutapp
Abhängigkeiten installieren:

Bash
npm install
▶️ 3. Server starten
Frontend und Backend müssen parallel gestartet werden. Sie benötigen dazu zwei separate Terminalfenster.

3.1 Backend starten (Terminal 1)

Stellen Sie sicher, dass die venv_django aktiviert ist und Sie sich im Wurzelverzeichnis (FrontendTryOutVue) befinden.

Bash
# Startet Django auf Port 8000
python manage.py runserver
Die API ist nun unter http://127.0.0.1:8000/ erreichbar.

3.2 Frontend starten (Terminal 2)

Wechseln Sie in das zweite Terminal und navigieren Sie in den Frontend-Ordner.

Bash
cd my-vue-Tryoutapp
# Startet den Vite Development Server (Standardmäßig Port 5173)
npm run dev
Die Anwendung ist nun im Browser unter http://localhost:5173/ verfügbar.

⚠️ Wichtiger Hinweis zur CORS-Konfiguration

Da das Frontend und das Backend auf unterschiedlichen Ports laufen, müssen Sie sicherstellen, dass das Django-Backend in seiner settings.py die CORS-Header korrekt konfiguriert hat, um Anfragen vom Frontend (Port 5173) zu erlauben. Dies ist für die Kommunikation zwischen Vue und Django erforderlich.