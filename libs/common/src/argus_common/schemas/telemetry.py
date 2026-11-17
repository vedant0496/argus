from enum import StrEnum
from typing import Annotated

from pydantic import AwareDatetime, Field

from argus_common.schemas.base import ArgusModel, Labels, Resource, TenantId

MetricName = Annotated[str, Field(pattern=r"^[a-zA-Z_:][a-zA-Z0-9_:.]{0,199}$")]


class MetricKind(StrEnum):
    GAUGE = "gauge"
    COUNTER = "counter"


class MetricPoint(ArgusModel):
    tenant_id: TenantId
    name: MetricName
    value: float = Field(allow_inf_nan=False)
    timestamp: AwareDatetime
    kind: MetricKind = MetricKind.GAUGE
    unit: str | None = Field(default=None, max_length=32)
    labels: Labels = Field(default_factory=dict)
    resource: Resource

    @property
    def series_key(self) -> str:
        """Stable identity of the time series this point belongs to."""
        labels = ",".join(f"{k}={v}" for k, v in sorted(self.labels.items()))
        host = self.resource.host or "-"
        return f"{self.tenant_id}|{self.resource.service}|{host}|{self.name}|{labels}"


class LogSeverity(StrEnum):
    TRACE = "trace"
    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"
    FATAL = "fatal"


class LogRecord(ArgusModel):
    tenant_id: TenantId
    timestamp: AwareDatetime
    severity: LogSeverity = LogSeverity.INFO
    body: str = Field(min_length=1, max_length=32_768)
    resource: Resource
    trace_id: str | None = Field(default=None, pattern=r"^[0-9a-f]{32}$")
    span_id: str | None = Field(default=None, pattern=r"^[0-9a-f]{16}$")
    attributes: Labels = Field(default_factory=dict)


class EventType(StrEnum):
    DEPLOYMENT = "deployment"
    CONFIG_CHANGE = "config_change"
    ALARM = "alarm"
    SCALING = "scaling"
    CUSTOM = "custom"


class Event(ArgusModel):
    """Discrete change events. These are strong signals for root-cause analysis."""

    tenant_id: TenantId
    timestamp: AwareDatetime
    type: EventType
    title: str = Field(min_length=1, max_length=256)
    description: str | None = Field(default=None, max_length=8_192)
    resource: Resource
    attributes: Labels = Field(default_factory=dict)
