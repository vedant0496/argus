from argus_common.config import ServiceSettings


class Settings(ServiceSettings):
    service_name: str = "rca-agent"
    http_port: int = 8003
