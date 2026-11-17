# Roadmap

Argus is built in two-week sprints. Each sprint ends with a working, demoable increment merged into `dev`. Every second sprint, `dev` is promoted to `main` and tagged.

| Sprint | Dates | Theme | Release |
|---|---|---|---|
| 0 | Nov 17 – Nov 22, 2026 | Foundations | — |
| 1 | Nov 23 – Dec 6, 2026 | Ingestion gateway | `v0.1.0` |
| 2 | Dec 7 – Dec 20, 2026 | Streaming anomaly detection | — |
| 3 | Dec 21, 2026 – Jan 3, 2027 | Persistence & incident correlation | `v0.2.0` |
| 4 | Jan 4 – Jan 17, 2027 | RCA agent (LLM + RAG) | — |
| 5 | Jan 18 – Jan 31, 2027 | Query API & dashboard | `v0.3.0` |
| 6 | Feb 1 – Feb 14, 2027 | Production hardening | `v1.0.0` |

---

## Sprint 0: Foundations

**Goal:** anyone can clone the repo, run `make check` and `make infra`, and get a green build.

- [x] ARG-1: uv workspace monorepo (`libs/*`, `services/*`)
- [x] ARG-2: `argus-common`: settings, structured logging, topic registry
- [x] ARG-3: canonical event schemas (metric, log, event, anomaly, incident)
- [x] ARG-4: messaging abstraction with in-memory broker for tests
- [x] ARG-5: service skeletons with health endpoints and a single parametrised Dockerfile
- [x] ARG-6: docker-compose: Redpanda, TimescaleDB, Redis, topic bootstrap
- [x] ARG-7: CI: ruff, mypy (strict), pytest + coverage, image build matrix
- [x] ARG-8: architecture doc, ADRs, contributing guide

## Sprint 1: Ingestion gateway

**Goal:** producers can push telemetry at high volume, safely.

- [ ] ARG-10: `POST /v1/{metrics,logs,events}` batch endpoints (≤ 5k items, partial-failure reporting)
- [ ] ARG-11: tenant API-key authentication (hashed keys, constant-time compare)
- [ ] ARG-12: per-tenant token-bucket rate limiting in Redis (atomic Lua script)
- [ ] ARG-13: Kafka publisher (aiokafka, idempotent producer, zstd, keyed by series for ordering)
- [ ] ARG-14: Prometheus metrics: accepted / rejected / throttled, publish latency
- [ ] ARG-15: Load test baseline (Locust), target ≥ 20k points/s per replica

## Sprint 2: Streaming anomaly detection

**Goal:** anomalies are emitted within seconds of a deviation.

- [ ] ARG-20: detector interface and registry
- [ ] ARG-21: EWMA z-score detector (online mean/variance, warm-up period)
- [ ] ARG-22: robust MAD detector over sliding windows (resistant to outliers)
- [ ] ARG-23: per-series state store with LRU eviction and bounded memory
- [ ] ARG-24: consumer loop with at-least-once semantics and manual commits
- [ ] ARG-25: debounce/hysteresis to avoid anomaly storms
- [ ] ARG-26: synthetic data generator + detector evaluation (precision/recall on labelled scenarios)

## Sprint 3: Persistence & incident correlation

**Goal:** related anomalies become one actionable incident.

- [ ] ARG-30: TimescaleDB schema + migrations (Alembic), hypertables, retention & compression policies
- [ ] ARG-31: metric/anomaly sink with batched COPY inserts
- [ ] ARG-32: service dependency topology model (static config → discovered from traces later)
- [ ] ARG-33: correlation engine: time-window + topology proximity + change-event boosting
- [ ] ARG-34: incident lifecycle (open → acknowledged → resolved, auto-resolve on recovery)
- [ ] ARG-35: severity scoring

## Sprint 4: RCA agent

**Goal:** every incident has a cited, ranked root-cause hypothesis within a minute.

- [ ] ARG-40: provider-agnostic LLM client (OpenAI, Anthropic, Ollama) with structured output
- [ ] ARG-41: agent tools: query metrics, search logs, list recent changes, get topology
- [ ] ARG-42: runbook ingestion + chunking + embeddings in pgvector
- [ ] ARG-43: plan/act loop with step budget, tool-call tracing and cost accounting
- [ ] ARG-44: evaluation harness with recorded incident scenarios
- [ ] ARG-45: guardrails: prompt-injection-safe tool outputs, PII redaction in logs

## Sprint 5: Query API & dashboard

**Goal:** operators can watch incidents unfold and read the agent's reasoning.

- [ ] ARG-50: incident / anomaly / series query endpoints with cursor pagination
- [ ] ARG-51: WebSocket live feed backed by the incidents topic
- [ ] ARG-52: Next.js dashboard: incident list, timeline, metric charts, RCA panel
- [ ] ARG-53: OIDC login, tenant scoping

## Sprint 6: Production hardening

**Goal:** deployable to Kubernetes with confidence.

- [ ] ARG-60: Helm chart, HPA on consumer lag (KEDA)
- [ ] ARG-61: OpenTelemetry tracing across services, Grafana dashboards
- [ ] ARG-62: end-to-end tests with Testcontainers
- [ ] ARG-63: load & chaos tests (broker loss, DB failover), published results
- [ ] ARG-64: v1.0 release notes and demo video
