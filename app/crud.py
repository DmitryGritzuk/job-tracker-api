from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Application, ApplicationStatus
from .schemas import ApplicationCreate, ApplicationPatch
from fastapi import HTTPException
from sqlalchemy.orm import Session

from .models import Application
from . import schemas


def patch_application(db: Session, app_id: int, payload: ApplicationUpdate) -> Application:
    obj = db.get(Application, app_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Application not found")

    data = payload.dict(exclude_unset=True)  # берем только то, что реально передали
    for key, value in data.items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj

def create_application(db: Session, data: ApplicationCreate) -> Application:
    a = Application(
        company=data.company,
        title=data.title,
        url=str(data.url) if data.url else None,
        status=data.status,
        notes=data.notes,
        tags=data.tags,
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


def get_application(db: Session, app_id: int) -> Optional[Application]:
    return db.get(Application, app_id)


def list_applications(
    db: Session,
    limit: int = 50,
    offset: int = 0,
    status: Optional[ApplicationStatus] = None,
    company: Optional[str] = None,
    q: Optional[str] = None,
) -> list:
    stmt = select(Application).order_by(Application.id.desc())

    if status is not None:
        stmt = stmt.where(Application.status == status)

    if company:
        stmt = stmt.where(Application.company.ilike(f"%{company}%"))

    if q:
        stmt = stmt.where(
            (Application.title.ilike(f"%{q}%")) | (Application.notes.ilike(f"%{q}%"))
        )

    stmt = stmt.limit(limit).offset(offset)
    return list(db.execute(stmt).scalars().all())


def update_application(db: Session, a: Application, payload: ApplicationPatch) -> Application:
    data = payload.model_dump(exclude_unset=True)  # pydantic v2

    for key, value in data.items():
        if key == "url" and value is not None:
            value = str(value)  # HttpUrl -> str
        setattr(a, key, value)

    db.commit()
    db.refresh(a)
    return a


def delete_application(db: Session, a: Application) -> None:
    db.delete(a)
    db.commit()