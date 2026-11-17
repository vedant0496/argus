from argus_common.config import ServiceSettings


class Settings(ServiceSettings):
    service_name: str = "api"
    http_port: int = 8000
