from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .db import get_db
from . import crud, schemas
from .models import ApplicationStatus

app = FastAPI(
    title="Job Tracker API",
    version="1.0.0",
    description="Мини-проект: CRUD для учета откликов на вакансии (FastAPI + SQLAlchemy + Alembic + Postgres/Docker).",
)


@app.get("/health", summary="Проверка здоровья сервиса", tags=["System"])
def health():
    return {"status": "ok"}


@app.post(
    "/applications",
    response_model=schemas.ApplicationOut,
    status_code=201,
    summary="Создать отклик",
    tags=["Applications"],
)
def create_application(payload: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    return crud.create_application(db, payload)


@app.get(
    "/applications",
    response_model=list[schemas.ApplicationOut],
    summary="Список откликов (фильтры + пагинация)",
    tags=["Applications"],
)
def list_applications(
    limit: int = Query(50, ge=1, le=100, description="Сколько записей вернуть (1–100)"),
    offset: int = Query(0, ge=0, description="Сколько записей пропустить"),
    status: Optional[ApplicationStatus] = Query(None, description="Фильтр по статусу"),
    company: Optional[str] = Query(None, description="Фильтр по компании (поиск по подстроке)"),
    q: Optional[str] = Query(None, description="Поиск по title/notes (по подстроке)"),
    db: Session = Depends(get_db),
):
    return crud.list_applications(db, limit=limit, offset=offset, status=status, company=company, q=q)


@app.get(
    "/applications/{app_id}",
    response_model=schemas.ApplicationOut,
    summary="Получить отклик по ID",
    tags=["Applications"],
)
def get_application(app_id: int, db: Session = Depends(get_db)):
    a = crud.get_application(db, app_id)
    if not a:
        raise HTTPException(status_code=404, detail="Application not found")
    return a


@app.patch(
    "/applications/{app_id}",
    response_model=schemas.ApplicationOut,
    summary="Частично обновить отклик (PATCH)",
    tags=["Applications"],
)
def patch_application(app_id: int, payload: schemas.ApplicationPatch, db: Session = Depends(get_db)):
    a = crud.get_application(db, app_id)
    if not a:
        raise HTTPException(status_code=404, detail="Application not found")
    return crud.update_application(db, a, payload)


@app.delete(
    "/applications/{app_id}",
    status_code=204,
    summary="Удалить отклик",
    tags=["Applications"],
)
def delete_application(app_id: int, db: Session = Depends(get_db)):
    a = crud.get_application(db, app_id)
    if not a:
        raise HTTPException(status_code=404, detail="Application not found")
    crud.delete_application(db, a)
    return None