# Threat Intelligence Log Analysis & Detection System

A full-stack threat intelligence platform for ingesting, parsing, and analyzing security logs with automated detection rules, alerting, and a real-time dashboard.

## Architecture

```
├── backend/          # Flask REST API
│   ├── app/          # Application code (routes, auth, detection engine)
│   ├── models/       # SQLAlchemy models (Log, Alert, User)
│   ├── tests/        # pytest test suite
│   └── static/       # Swagger/OpenAPI spec
├── dashboard/        # Static HTML/JS dashboard (Chart.js)
└── docker-compose.yml
```

## Tech Stack

- **Backend:** Python 3.12+, Flask, SQLAlchemy, PyMongo, Celery
- **Databases:** PostgreSQL (structured data), MongoDB (raw logs)
- **Queue:** Redis + Celery (async log processing)
- **Frontend:** HTML/JS dashboard with Chart.js
- **Auth:** JWT-based authentication with RBAC
- **CI/CD:** GitHub Actions (flake8 lint + pytest)

## Quick Start

### Local Development

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\Activate.ps1  # Windows PowerShell

# Install dependencies
pip install -r backend/requirements.txt

# Run tests
TESTING=1 PYTHONPATH=backend pytest backend/tests -v

# Start dev server
cd backend
TESTING=1 flask --app app run --debug --port 5000
```

### Docker (Production)

```bash
docker-compose up -d --build
```

## API Endpoints

All API routes are prefixed with `/api`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/upload-log` | Upload a log file for processing |
| GET | `/api/logs/status` | Check log processing status |
| GET | `/api/logs/<id>` | Retrieve a raw log by ID |
| DELETE | `/api/logs/<id>` | Delete a raw log by ID |
| GET | `/api/events` | View parsed/structured events |
| GET | `/api/alerts` | View generated alerts |
| POST | `/api/detect` | Trigger detection engine |
| GET | `/api/dashboard` | Dashboard summary data |
| GET | `/api/metrics` | Prometheus metrics |
| POST | `/register` | Register a new user |
| POST | `/login` | Authenticate and get JWT token |

## Dashboard

The dashboard is served at the root `/` and provides:
- Real-time alert and event counts
- Chart.js visualizations of threat activity
- Log upload interface

## Testing

```bash
# Run all tests (7 tests)
TESTING=1 PYTHONPATH=backend pytest backend/tests -v

# Lint
flake8 backend/app backend/models
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_URI` | PostgreSQL connection string | — |
| `MONGO_URI` | MongoDB connection string | — |
| `SECRET_KEY` | JWT signing key (min 32 chars) | — |
| `TESTING` | Enable test mode (mocks Celery/Mongo) | `0` |
| `REDIS_URL` | Redis URL for Celery broker | `redis://localhost:6379/0` |

See `backend/.env.example` for a template.

## License

MIT
