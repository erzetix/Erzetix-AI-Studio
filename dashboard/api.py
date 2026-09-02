"""
Точки входа дашборда клиента.

Реализация операций, подключение к оркестратору и проверка учётных
данных пользователей находятся в закрытой ветке разработки и не входят
в состав публичного репозитория.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .models import (
    ApprovalDecision,
    ApprovalMode,
    CampaignView,
    MaterialView,
    PublicationMetrics,
    UserRole,
)

# Операции, доступные каждой роли пользователя. Операция, отсутствующая
# в перечне роли, отклоняется с кодом FORBIDDEN.
ROLE_PERMISSIONS: dict[UserRole, tuple[str, ...]] = {
    UserRole.CLIENT: (
        "create_campaign",
        "list_campaigns",
        "get_campaign",
        "list_materials",
        "approve_material",
        "reject_material",
        "get_metrics",
        "get_report",
        "get_character_profile",
    ),
    UserRole.CONTENT_SPECIALIST: (
        "list_campaigns",
        "get_campaign",
        "list_materials",
        "approve_material",
        "reject_material",
        "submit_metrics",
        "get_metrics",
        "get_report",
    ),
    UserRole.GUEST: (
        "list_campaigns",
        "get_campaign",
        "list_materials",
    ),
}


@dataclass
class DashboardConfig:
    """Конфигурация дашборда."""

    name: str = "dashboard"
    default_approval_mode: ApprovalMode = ApprovalMode.MANUAL
    guest_mode_enabled: bool = True
    guest_demo_campaign_ids: list[str] = field(default_factory=list)


class DashboardAPI:
    """
    Перечень операций дашборда клиента.

    Реализация методов ниже находится в закрытой ветке разработки
    и не входит в состав публичного репозитория.
    """

    def __init__(self, config: DashboardConfig | None = None) -> None:
        self.config = config or DashboardConfig()

    # --- Кампании -------------------------------------------------------

    def create_campaign(self, brief: "Brief", role: UserRole) -> CampaignView:  # noqa: F821
        """POST /campaigns — создание кампании на основании брифа."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def list_campaigns(self, role: UserRole) -> list[CampaignView]:
        """GET /campaigns — получение списка кампаний, доступных роли."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def get_campaign(self, campaign_id: str, role: UserRole) -> CampaignView:
        """GET /campaigns/{campaign_id} — получение состояния кампании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    # --- Материалы ------------------------------------------------------

    def list_materials(self, campaign_id: str, role: UserRole) -> list[MaterialView]:
        """GET /campaigns/{campaign_id}/materials — получение материалов кампании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def approve_material(self, material_id: str, role: UserRole) -> ApprovalDecision:
        """POST /materials/{material_id}/approve — утверждение материала."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def reject_material(
        self,
        material_id: str,
        reason: str,
        role: UserRole,
    ) -> ApprovalDecision:
        """POST /materials/{material_id}/reject — отклонение материала."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    # --- Показатели эффективности ---------------------------------------

    def submit_metrics(self, metrics: PublicationMetrics, role: UserRole) -> None:
        """POST /campaigns/{campaign_id}/metrics — ввод показателей публикации."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def get_metrics(self, campaign_id: str, role: UserRole) -> list[PublicationMetrics]:
        """GET /campaigns/{campaign_id}/metrics — получение показателей кампании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def get_report(self, campaign_id: str, role: UserRole) -> dict:
        """GET /campaigns/{campaign_id}/report — формирование отчёта об эффективности."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    # --- Профиль персонажа ----------------------------------------------

    def get_character_profile(self, character_id: str, role: UserRole) -> dict:
        """GET /characters/{character_id} — получение профиля персонажа."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    # --- Разграничение доступа ------------------------------------------

    def is_permitted(self, role: UserRole, operation: str) -> bool:
        """Проверяет доступность операции для роли пользователя."""
        return operation in ROLE_PERMISSIONS.get(role, ())
