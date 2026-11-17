# Contributing

## Branching

| Branch | Purpose |
|---|---|
| `main` | Released code only. Tagged on every release. |
| `dev` | Integration branch. Always green. Every PR targets it. |
| `feature/<short-name>` | One story or a tightly related set from the [roadmap](docs/roadmap.md). |
| `fix/<short-name>` | Bug fixes. |

1. Branch off the latest `dev`.
2. Keep commits small and focused. Use [Conventional Commits](https://www.conventionalcommits.org/) (`feat(ingestion): ...`, `fix(common): ...`, `docs: ...`).
3. Run `make check` before pushing.
4. Open a PR into `dev` using the template and reference the roadmap item (`ARG-12`).
5. Squash-merge once CI is green and the PR is reviewed.

`dev` is merged into `main` at the end of each release sprint.

## Local setup

```bash
make install
make check
```

## Adding a service

1. `services/<name>/pyproject.toml` with `argus-common = { workspace = true }`.
2. Package under `src/argus_<name>/` with a console script `argus-<name>`.
3. Add it to the root `pyproject.toml` dependencies, the mypy path, the CI image matrix and `docker-compose.yml`.

## Schemas

Event schemas in `libs/common/src/argus_common/schemas` are a public contract. Breaking changes require a new topic version (`*.v2`) and a migration note in the PR.
