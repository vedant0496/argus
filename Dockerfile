# One image definition for every Python service; pick the service with --build-arg SERVICE=<name>.
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app
ARG SERVICE
COPY pyproject.toml uv.lock ./
COPY libs libs
COPY services services
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable --package argus-${SERVICE}

FROM python:3.12-slim
ARG SERVICE
ENV SERVICE=${SERVICE} PATH="/app/.venv/bin:${PATH}" PYTHONUNBUFFERED=1
RUN useradd --create-home --uid 10001 argus
COPY --from=builder --chown=argus:argus /app/.venv /app/.venv
USER argus
CMD ["sh", "-c", "exec argus-${SERVICE}"]
