# [ STRIKE 1v1 ] - Counter Strike 1.6 Website Platform

**Strike 1v1** is a web application built with Django, designed to manage and facilitate 1v1 matchmaking through a web platform for Counter-Strike 1.6. This project integrates a "Retro" user interface with a backend logic to provide a great experience for the players.

## Repository Objective

The primary objective of this repository is to host the website of the Strike 1v1 platform:
- **Matchmaking Logic:** Managing player statistics (ELO, K/D, Winrate) through the relational model database.
- **Containerized Deployment:** Using Docker and the 12-Factor App methodology.
- **Academic Exploration:** All this is learning workflow for mastering the Django framework and modern DevOps pipelines.

## Technology Stack

* **Backend:** Django 6.x (Python)
* **Frontend:** Tailwind CSS and HTML
* **Package Manager:** [uv](https://github.com/astral-sh/uv) (High-performance package resolver)
* **Orchestration:** Docker & Docker-Compose
* **Web Server:** Gunicorn (WSGI)

## Run/Deploy Instructions

Follow these steps to run the application in a local environment.

### 1. Prerequisites
Ensure you have the following installed on your host machine:
- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/) (For Docker deployment)
- [uv](https://github.com/astral-sh/uv) (For local development)

### 2. Clone the Repository

```bash
git clone https://github.com/MarcPujolUNI/Strike1v1.git
cd Strike1v1
```

### 3. Environment Configuration

The application uses environment variables for configuration. While default values are provided for easy development, you can create a `.env` file in the root directory for custom settings as the following one:

```Bash
DEBUG=True
SECRET_KEY=your-secure-secret-key
```

**Note:** If you set `DEBUG=False`, Django will not serve static files (CSS/images) via the standard `runserver` command. It is highly recommended to keep `DEBUG=True` for local development, or use the Docker setup which handles static files automatically.

### 4. Run the application

#### Option A: Run with Docker (Recommended)

This is the fastest way to get the project running. Docker will build the image, install dependencies using uv, and start the server.

```Bash
docker-compose up --build
```

The container's `entrypoint.sh` will automatically:

1. Run database migrations (`python manage.py migrate`).

2. Collect static assets (`python manage.py collectstatic`).

3. Launch the Gunicorn server on port 8000.

Open your browser and navigate to: http://localhost:8000

#### Option B: Run Locally (Development Mode)

If you prefer to run the application directly on your machine without Docker:

1. Synchronize dependencies:

    ```Bash
    uv sync
    ```
   
2. Apply database migrations:

    ```Bash
    uv run python manage.py migrate
    ```
   
3. Start the development server:

    ```Bash
    uv run python manage.py runserver
    ```

Open your browser and navigate to: http://localhost:8000

# Contributions & Academic Disclaimer

This project is part of a learning workflow. All features and code implementations are primarily for academic purposes. There is currently no intention to deploy this version into a commercial production environment.