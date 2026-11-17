from argus_common.config import ServiceSettings


class Settings(ServiceSettings):
    service_name: str = "ingestion"
    http_port: int = 8001
