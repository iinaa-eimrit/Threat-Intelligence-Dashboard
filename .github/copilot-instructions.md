# Threat Intelligence Log Analysis & Detection System

## Project Overview
- **Type:** Python / Flask web application
- **Language:** Python 3.12+
- **Frameworks:** Flask, SQLAlchemy, PyMongo, Celery
- **Database:** PostgreSQL (structured data), MongoDB (raw logs)
- **Frontend:** Static HTML/JS dashboard (Chart.js)
- **CI/CD:** GitHub Actions (lint + test)

## Project Setup Checklist
- [x] Verify that the copilot-instructions.md file in the .github directory is created.
- [x] Clarify Project Requirements
- [x] Scaffold the Project
- [x] Customize the Project
- [x] Install Required Extensions (skipped — none needed)
- [x] Compile the Project
- [x] Create and Run Task (skipped — Flask dev server used directly)
- [x] Launch the Project
- [x] Ensure Documentation is Complete

## Development Commands
- **Install dependencies:** `pip install -r backend/requirements.txt`
- **Run tests:** `TESTING=1 PYTHONPATH=backend pytest backend/tests -v`
- **Lint:** `flake8 backend/app backend/models`
- **Run dev server:** `TESTING=1 PYTHONPATH=backend flask --app app run --debug --port 5000` (from `backend/`)
- **Docker:** `docker-compose up -d --build`

## Key Directories
- `backend/app/` — Flask application (routes, auth, detection engine, extensions)
- `backend/models/` — SQLAlchemy models (Log, Alert, User)
- `backend/tests/` — pytest test suite (7 tests)
- `dashboard/` — Static HTML/JS dashboard
- `.github/workflows/` — CI pipeline

Before starting a new task in the above plan, update progress in the plan.
-->
- Work through each checklist item systematically.
- Keep communication concise and focused.
- Follow development best practices.
