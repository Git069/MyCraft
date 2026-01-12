# MyCraft - Handwerker-Marktplatz

MyCraft ist eine moderne Webanwendung, die als Marktplatz für Handwerksdienstleistungen dient. Sie verbindet Kunden mit professionellen Handwerkern und ermöglicht eine nahtlose Kommunikation und Auftragsabwicklung.

## 🚀 Features

- **Benutzer-Authentifizierung:** Registrierung, Login, Token-basierte Authentifizierung (Djoser).
- **Rollen-System:** Unterscheidung zwischen normalen Nutzern (Kunden) und Handwerkern.
- **Auftrags-Marktplatz:** Handwerker können Angebote erstellen; Kunden können diese durchsuchen und filtern (Geo-Suche unterstützt).
- **Interaktives Messaging:** Ein Echtzeit-Chat-System für die Kommunikation zwischen Kunden und Handwerkern.
- **Angebotssystem:** Verbindliche Angebote im Chat, die Kunden annehmen oder ablehnen können.
- **Profilverwaltung:** Bearbeitung von Profildaten und Upload von Profilbildern.
- **Dashboard:** Persönlicher Bereich zur Verwaltung von Angeboten und Buchungen.

## 🛠 Technische Architektur

### Backend
- **Framework:** Django & Django REST Framework
- **Datenbank:** PostGIS (PostgreSQL mit GIS-Erweiterung)
- **Authentifizierung:** Djoser & TokenAuthentication
- **Containerisierung:** Docker & Docker Compose
- **Tools:** `django-filter`, `Pillow`

### Frontend
- **Framework:** Vue 3 (Composition API)
- **Build-Tool:** Vite
- **State Management:** Pinia
- **Routing:** Vue Router
- **HTTP Client:** Axios
- **Styling:** CSS Variablen, Flexbox & Grid

---

## ⚙️ Installation & Einrichtung

Das Projekt ist vollständig dockerisiert. Befolgen Sie diese Schritte, um die Entwicklungsumgebung zu starten.

### 1. Voraussetzungen
- [Docker](https://www.docker.com/) und Docker Compose müssen installiert sein.
- Git

### 2. Repository klonen
```bash
git clone [URL_DEINES_REPOS]
cd MyCraft

```

### 3. Umgebungsvariablen (.env) konfigurieren

Das Projekt benötigt zwei `.env` Dateien: eine für das Backend und eine für das Frontend.

#### Backend (`backend/.env`)

Erstellen Sie im Ordner `backend/` eine Datei namens `.env` und füllen Sie sie mit folgenden Werten:

```ini
# --- Django Einstellungen ---
# Setzen Sie DEBUG für die lokale Entwicklung auf True
DJANGO_DEBUG=True

# Ein zufälliger geheimer Schlüssel (für Dev reicht ein beliebiger String)
DJANGO_SECRET_KEY=django-insecure-dev-key-change-me

# Erlaubte Hosts (für Docker Umgebung)
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,backend

# CORS Einstellungen (URL des Frontends)
DJANGO_CORS_ALLOWED_ORIGINS=http://localhost:5173,[http://127.0.0.1:5173](http://127.0.0.1:5173)

# --- Datenbank Einstellungen (müssen mit docker-compose übereinstimmen) ---
POSTGRES_DB=mycraft_dev
POSTGRES_USER=mycraft_user
POSTGRES_PASSWORD=mycraft_password
DB_HOST=db
DB_PORT=5432

# --- Google Gemini AI ---
GEMINI_API_KEY=hier_deinen_google_api_key_einfuegen

```

#### Frontend (`frontend/web_app/.env`)

Erstellen Sie im Ordner `frontend/web_app/` eine Datei namens `.env`:

```ini
# URL der Backend API
VITE_API_URL=http://localhost:8000/api

```

---

### 4. Anwendung starten

Verwenden Sie Docker Compose, um die Container zu bauen und zu starten. Das Flag `--profile develop` aktiviert auch den Frontend-Dev-Server.

```bash
docker-compose --profile develop up --build

```

### 5. Datenbank initialisieren

Sobald die Container laufen, müssen die Datenbank-Migrationen angewendet werden. Öffnen Sie ein **neues Terminal** im Projektverzeichnis:

```bash
# Migrationen ausführen
docker-compose exec backend python manage.py migrate

# (Optional) Superuser für den Admin-Bereich erstellen
docker-compose exec backend python manage.py createsuperuser

```

### 6. Zugriff auf die Anwendung

* **Frontend:** [http://localhost:5173](https://www.google.com/search?q=http://localhost:5173)
* **Backend API:** [http://localhost:8000/api/](https://www.google.com/search?q=http://localhost:8000/api/)
* **Admin Panel:** [http://localhost:8000/admin/](https://www.google.com/search?q=http://localhost:8000/admin/)

---

## 📦 Wichtige Befehle

| Aktion | Befehl |
| --- | --- |
| **Starten** | `docker-compose --profile develop up` |
| **Stoppen** | `docker-compose down` |
| **Alles löschen (inkl. Volumes)** | `docker-compose down -v` |
| **Migrationen erstellen** | `docker-compose exec backend python manage.py makemigrations` |
| **Migrationen anwenden** | `docker-compose exec backend python manage.py migrate` |
| **Logs anzeigen** | `docker-compose logs -f backend` |

## 🧪 Tests ausführen

Backend-Tests:

```bash
docker-compose exec backend python manage.py test

```

```

### 2. Die `.env` Dateien anlegen

Wie in der neuen README beschrieben, müssen Sie nun noch die Konfigurationsdateien erstellen, damit Docker startet.

1.  **Backend:**
    * Gehen Sie in den Ordner `backend/`.
    * Erstellen Sie eine Datei namens `.env`.
    * Kopieren Sie den Inhalt aus dem Abschnitt **"Backend (backend/.env)"** der README oben hinein.

2.  **Frontend:**
    * Gehen Sie in den Ordner `frontend/web_app/`.
    * Erstellen Sie eine Datei namens `.env`.
    * Kopieren Sie den Inhalt aus dem Abschnitt **"Frontend (frontend/web_app/.env)"** der README oben hinein.

Sobald Sie diese drei Dateien (`README.md`, `backend/.env`, `frontend/web_app/.env`) erstellt haben, können Sie `docker-compose --profile develop up --build` ausführen und loslegen!

```