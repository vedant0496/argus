from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

TenantId = Annotated[str, Field(pattern=r"^[a-z0-9][a-z0-9-]{1,62}$")]
Labels = Annotated[dict[str, str], Field(max_length=64)]


class ArgusModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)


class Resource(ArgusModel):
    """The entity that emitted a signal: a service instance, a network element, a host."""

    service: str = Field(min_length=1, max_length=128)
    host: str | None = Field(default=None, max_length=255)
    region: str | None = Field(default=None, max_length=64)
    attributes: Labels = Field(default_factory=dict)
