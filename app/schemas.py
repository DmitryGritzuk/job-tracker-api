from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl

from .models import ApplicationStatus


class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=200)
    url: Optional[HttpUrl] = None
    status: ApplicationStatus = ApplicationStatus.applied
    notes: Optional[str] = None
    tags: Optional[str] = Field(default=None, description='Comma-separated, e.g. "python,fastapi,remote"')


class ApplicationPatch(BaseModel):
    company: Optional[str] = Field(default=None, min_length=1, max_length=200)
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    url: Optional[HttpUrl] = None
    status: Optional[ApplicationStatus] = None
    notes: Optional[str] = None
    tags: Optional[str] = None


class ApplicationOut(BaseModel):
    id: int
    company: str
    title: str
    url: Optional[str]
    status: ApplicationStatus
    notes: Optional[str]
    tags: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}