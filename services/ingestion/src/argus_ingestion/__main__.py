import uvicorn

from argus_common.logging import configure_logging
from argus_ingestion.app import create_app
from argus_ingestion.config import Settings


def main() -> None:
    settings = Settings()
    configure_logging(settings.log_level, json=settings.log_json)
    uvicorn.run(create_app(settings), host=settings.http_host, port=settings.http_port)


if __name__ == "__main__":
    main()
