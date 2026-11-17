from fastapi import FastAPI

from argus_api.config import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    app = FastAPI(title="Argus api", version="0.1.0")
    app.state.settings = settings

    @app.get("/healthz", include_in_schema=False)
    async def healthz() -> dict[str, str]:
        return {"status": "ok", "service": settings.service_name}

    return app
