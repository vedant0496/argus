import asyncio

from argus_common.logging import configure_logging, get_logger
from argus_common.runtime import wait_for_shutdown
from argus_incidents.config import Settings


async def run(settings: Settings) -> None:
    log = get_logger(settings.service_name)
    log.info("worker.started", environment=settings.environment)
    await wait_for_shutdown()
    log.info("worker.stopped")


def main() -> None:
    settings = Settings()
    configure_logging(settings.log_level, json=settings.log_json)
    asyncio.run(run(settings))


if __name__ == "__main__":
    main()
