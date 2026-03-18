# Threat Intelligence Log Analysis & Detection System - Backend

## Features
- Flask REST API for log ingestion and status
- PostgreSQL (SQLAlchemy) for structured data
- MongoDB (PyMongo) for raw logs
- Dockerized for easy deployment

## Setup (Development)
1. Copy `.env.example` to `.env` and fill in your secrets.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask app:
   ```bash
   flask run
   ```

## Docker Compose (Recommended for Production)
Build and run the full stack (backend, Postgres, MongoDB):
```bash
docker-compose up -d --build
```
Stop all services:
```bash
docker-compose down
```

## API Endpoints
- `POST /upload-log` - Upload log file (multipart/form-data)
- `GET /logs/status` - Check log processing status
- `GET /logs/<log_id>` - Retrieve a raw log by ID
- `DELETE /logs/<log_id>` - Delete a raw log by ID
- `GET /events` - View parsed/structured events
- `GET /alerts` - View generated alerts
- `POST /detect` - Trigger detection engine

## Dashboard
- Open `dashboard/index.html` in your browser to view alerts and events.
- For production, serve the dashboard via Flask static files or a web server (nginx).
## API Documentation
- Swagger UI available at [`/docs`](http://localhost:5000/docs) (see `swagger.json` for endpoint details)
- OpenAPI/Swagger JSON: `backend/static/swagger.json`

## Authentication & Security
- JWT-based authentication for user endpoints (`/register`, `/login`)
- Role-based access control (RBAC) for sensitive actions
- Rate limiting and CORS enabled
- Audit logging for user actions

## Monitoring & Alerting
- Prometheus metrics exposed for backend monitoring
- Grafana dashboard for visualization (see `docker-compose.yml` for setup)
- Alert notifications via email, Slack, or webhook (configurable in `alert_notify.py`)


## Project Structure
- `app/` - Flask app code
- `models/` - SQLAlchemy models
- `dashboard/` - Dashboard HTML/JS
- `config.py` - Configuration
- `requirements.txt` - Python dependencies
- `Dockerfile` - Containerization
- `docker-compose.yml` - Multi-service orchestration
- `.env.example` - Environment variable template
