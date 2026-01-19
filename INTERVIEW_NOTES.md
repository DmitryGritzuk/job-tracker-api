# Job Tracker API — interview notes

## 1) Что это
Небольшой REST API для учета откликов на вакансии (CRUD).

Цель: показать базовый backend-набор:
- FastAPI + SQLAlchemy
- миграции Alembic
- Postgres + Docker Compose
- тесты Pytest

## 2) Что реализовано
### Endpoints
- GET /health
- POST /applications
- GET /applications (pagination + filters)
- GET /applications/{id}
- PATCH /applications/{id}  (частичное обновление)
- DELETE /applications/{id}

Swagger: /docs

## 3) Почему PATCH сделан “правильно”
PATCH = частичное обновление.  
То есть клиент может прислать только одно поле, например:
{ "status": "interview" }

В коде это делается так:
- схема PATCH — все поля Optional
- в update берём только реально переданные поля:
  `exclude_unset=True`
- обновляем только их, остальные не трогаем

## 4) Валидации и ошибки
- 404 если записи нет (например PATCH /applications/9999)
- 422 если app_id не int или тело запроса невалидно (Pydantic)

## 5) Тесты (pytest)
Проверяю основные сценарии:
- создание и список
- PATCH меняет только одно поле
- PATCH not found → 404
- DELETE → 204

Тестовая БД: SQLite (быстро, изолировано), через dependency override `get_db`.

## 6) Как запустить (кратко)
### Docker (рекомендуется)
docker compose up --build

### Локально (venv)
- создать .env из .env.example
- поднять Postgres
- alembic upgrade head
- uvicorn app.main:app --reload --port 8000