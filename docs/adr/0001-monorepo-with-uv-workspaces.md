# ADR 0001: Monorepo with uv workspaces

- **Status:** accepted
- **Date:** 2026-11-17

## Context

Argus has several Python services that share event schemas. Schema drift between producer and consumer is the most likely source of production bugs.

## Decision

Use a single repository with a [uv workspace](https://docs.astral.sh/uv/concepts/workspaces/). Shared code lives in `libs/`. Each deployable lives in `services/<name>` with its own `pyproject.toml` and dependencies. One lockfile pins the whole system.

## Consequences

- Schema changes and all their consumers ship in one PR and one CI run.
- Each service image installs only its own dependency closure (`uv sync --package`).
- CI time grows with the repo. We will add path-based job filtering once it passes ~5 minutes.
