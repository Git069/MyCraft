# MyCraft - Handwerker-Marktplatz

MyCraft ist eine moderne Webanwendung, die als Marktplatz für Handwerksdienstleistungen dient. Sie verbindet Kunden mit professionellen Handwerkern und ermöglicht eine nahtlose Kommunikation und Auftragsabwicklung.

## Features

- **Benutzer-Authentifizierung:** Registrierung, Login, Token-basierte Authentifizierung.
- **Rollen-System:** Unterscheidung zwischen normalen Nutzern (Kunden) und Handwerkern.
- **Auftrags-Marktplatz:** Handwerker können Angebote erstellen, Kunden können diese durchsuchen und filtern.
- **Interaktives Messaging:** Ein Echtzeit-Chat-System mit Short-Polling für die Kommunikation zwischen Kunden und Handwerkern.
- **Angebotssystem:** Handwerker können im Chat verbindliche Angebote erstellen, die Kunden annehmen oder ablehnen können.
- **Profilverwaltung:** Nutzer können ihre Profildaten bearbeiten und ein Profilbild hochladen.
- **Dashboard:** Ein persönlicher Bereich für Nutzer, um ihre Angebote und Buchungen zu verwalten.

## Technische Architektur

### Backend
- **Framework:** Django & Django REST Framework
- **Datenbank:** SQLite (Entwicklung), PostgreSQL (Produktion)
- **Authentifizierung:** Djoser & TokenAuthentication
- **API-Dokumentation:** API Root (`/`)
- **Sonstiges:** `django-filter` für die Filterung, `Pillow` für Bildverarbeitung.

### Frontend
- **Framework:** Vue 3 (Composition API)
- **Build-Tool:** Vite
- **State Management:** Pinia
- **Routing:** Vue Router
- **API-Kommunikation:** Axios
- **Styling:** Modernes CSS mit Variablen, Flexbox & Grid.

## Lokale Entwicklungsumgebung

Das Projekt verwendet Docker und Docker Compose, um die Entwicklungsumgebung zu verwalten.

### Voraussetzungen
- Docker
- Docker Compose

### Starten der Anwendung

1. **Klone das Repository:**
   ```sh
   git clone [URL_DEINES_REPOS]
   cd MyCraft
   ```

2. **Starte die Docker-Container:**
   Der `--profile develop`-Flag startet die Entwicklungskonfiguration (inkl. Frontend Dev-Server).
   ```sh
   docker-compose --profile develop up --build
   ```

3. **Datenbank-Migrationen anwenden:**
   Öffne ein **zweites Terminal** und führe die Migrationen aus, um das Datenbankschema zu erstellen/aktualisieren.
   ```sh
   docker-compose exec backend python manage.py migrate
   ```

4. **Anwendung öffnen:**
   - **Frontend:** [http://localhost:5173](http://localhost:5173)
   - **Backend API:** [http://localhost:8000/api/](http://localhost:8000/api/)

### Wichtige Befehle

- **Anwendung stoppen:** `docker-compose down`
- **Anwendung stoppen & Volumes löschen:** `docker-compose down -v` (Nützlich bei Caching-Problemen)
- **Migrationen erstellen:** `docker-compose exec backend python manage.py makemigrations`
- **Superuser erstellen:** `docker-compose exec backend python manage.py createsuperuser`
- **Logs anzeigen:** `docker-compose logs -f [backend|frontend]`
