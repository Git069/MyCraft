# MyCraft Project

This project is a web application with a Django backend and a Vue.js frontend. It is fully containerized using Docker.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Git](https://git-scm.com/downloads)

## Getting Started

1. **Clone the repository:**
   ```sh
   git clone <your-repository-url>
   cd MyCraft
   ```

2. **Run the application:**
   Use the following command to build and run the entire application:
   ```sh
   docker-compose --profile develop up --build
   ```

   This will start both the backend and frontend services in development mode with live-reloading enabled.

## Accessing the Application

- **Frontend:** [http://localhost:8080](http://localhost:8080)
- **Backend API:** [http://localhost:8000](http://localhost:8000)

## Project Structure

- `backend/`: Contains the Django backend application.
- `frontend/`: Contains the Vue.js frontend application.
- `docker-compose.yml`: Defines the services, networks, and volumes for the Docker application.
