# Job Tracker API (FastAPI)

Simple REST API to track job applications.

## Stack
- FastAPI
- SQLAlchemy
- Alembic (migrations)
- PostgreSQL
- Docker + Docker Compose
- Pytest

## Features
- Create application
- List applications (filters + pagination)
- Patch (partial update)
- Delete application
- Swagger UI: `/docs`

---

## Run locally (venv)

### 1) Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

2) Setup env

Create .env file:
cp .env.example .env

Edit .env and set:
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/jobtracker

3) Run PostgreSQL (Docker)
docker compose up -d db

4) Run migrations
alembic upgrade head

5) Run API
uvicorn app.main:app --reload --port 8000

Open Swagger UI:
http://127.0.0.1:8000/docs

Run with Docker Compose (recommended)
docker compose up --build

Swagger UI:
http://127.0.0.1:8000/docs

Run tests
pytest -q

API Endpoints
	•	GET /health
	•	POST /applications
	•	GET /applications?limit=50&offset=0
	•	GET /applications/{id}
	•	PATCH /applications/{id}
	•	DELETE /applications/{id}

    ---

## ✅ Как залить README на GitHub

В терминале:

```bash
git add README.md
git commit -m "Update README"
git push