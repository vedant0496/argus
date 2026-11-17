from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import AwareDatetime, Field

from argus_common.schemas.base import ArgusModel, Labels, Resource, TenantId


def _now() -> datetime:
    return datetime.now(UTC)


class Direction(StrEnum):
    UP = "up"
    DOWN = "down"


class Anomaly(ArgusModel):
    id: UUID = Field(default_factory=uuid4)
    tenant_id: TenantId
    series_key: str
    metric_name: str
    resource: Resource
    labels: Labels = Field(default_factory=dict)
    observed_at: AwareDatetime
    value: float
    expected: float
    score: float = Field(ge=0, description="Detector-specific deviation score, higher is worse")
    direction: Direction
    detector: str
    detected_at: AwareDatetime = Field(default_factory=_now)


class Severity(StrEnum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    WARNING = "warning"


class IncidentStatus(StrEnum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class RootCauseHypothesis(ArgusModel):
    summary: str
    confidence: float = Field(ge=0, le=1)
    evidence: list[str] = Field(default_factory=list)
    suggested_actions: list[str] = Field(default_factory=list)


class Incident(ArgusModel):
    id: UUID = Field(default_factory=uuid4)
    tenant_id: TenantId
    title: str
    status: IncidentStatus = IncidentStatus.OPEN
    severity: Severity
    opened_at: AwareDatetime = Field(default_factory=_now)
    updated_at: AwareDatetime = Field(default_factory=_now)
    resolved_at: AwareDatetime | None = None
    anomaly_ids: list[UUID] = Field(default_factory=list)
    affected_services: list[str] = Field(default_factory=list)
    root_cause: RootCauseHypothesis | None = None
