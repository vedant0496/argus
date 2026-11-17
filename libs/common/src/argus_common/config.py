from enum import StrEnum

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    LOCAL = "local"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


class ServiceSettings(BaseSettings):
    """Base settings shared by every service. Services subclass this and add their own fields."""

    model_config = SettingsConfigDict(env_prefix="ARGUS_", env_file=".env", extra="ignore")

    service_name: str = "argus"
    environment: Environment = Environment.LOCAL
    log_level: str = "INFO"
    log_json: bool = False

    kafka_bootstrap_servers: str = "localhost:19092"
    redis_url: str = "redis://localhost:6379/0"
    database_url: str = "postgresql://argus:argus@localhost:5432/argus"

    http_host: str = "0.0.0.0"
    http_port: int = Field(default=8000, ge=1, le=65535)

    @property
    def is_production(self) -> bool:
        return self.environment is Environment.PRODUCTION
