"""
Модели данных дашборда клиента.

Учётные данные пользователей и требования брендов клиентов относятся
к защищаемым сведениям и не входят в состав данного модуля.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class UserRole(str, Enum):
    """Роль пользователя дашборда."""

    CLIENT = "client"
    CONTENT_SPECIALIST = "content_specialist"
    GUEST = "guest"


class ApprovalMode(str, Enum):
    """Режим утверждения материалов."""

    MANUAL = "manual"
    HYBRID = "hybrid"
    AUTONOMOUS = "autonomous"


class MaterialState(str, Enum):
    """Состояние материала в контуре утверждения."""

    IN_PRODUCTION = "in_production"
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"


class MaterialView(BaseModel):
    """Представление материала для интерфейса дашборда."""

    material_id: str
    campaign_id: str
    draft_id: str
    format: str
    state: MaterialState
    preview_ref: str
    caption: str | None = None
    guardian_verdict: str | None = None
    failed_checks: list[str] = Field(default_factory=list)
    created_at: datetime


class CampaignView(BaseModel):
    """Представление кампании для интерфейса дашборда."""

    campaign_id: str
    character_id: str
    title: str
    state: str
    approval_mode: ApprovalMode
    materials_total: int = Field(ge=0, default=0)
    materials_awaiting_approval: int = Field(ge=0, default=0)
    created_at: datetime
    updated_at: datetime
    state_observed_at: datetime | None = None


class ApprovalDecision(BaseModel):
    """Решение об утверждении или отклонении материала."""

    material_id: str
    approved: bool
    decided_by: str
    decided_at: datetime
    rejection_reason: str | None = None


class PublicationMetrics(BaseModel):
    """Показатели эффективности публикации, вводимые специалистом."""

    material_id: str
    platform: str
    published_at: datetime
    views: int = Field(ge=0)
    reactions: int = Field(ge=0)
    comments: int = Field(ge=0)
    shares: int = Field(ge=0)
    reported_by: str
