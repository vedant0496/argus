# ADR 0003: TimescaleDB for time series, incidents and embeddings

- **Status:** accepted
- **Date:** 2026-11-17

## Context

We need time-series storage for samples, relational storage for incidents, and vector search for runbook RAG.

## Decision

Use PostgreSQL with the TimescaleDB extension (hypertables, compression, retention policies) and pgvector for embeddings. Run one engine instead of three.

## Consequences

- Joins across incidents, anomalies and samples are plain SQL.
- At very high cardinality we may move raw samples to a dedicated TSDB (e.g. VictoriaMetrics). The processor sink is isolated behind a repository interface so the move stays local.
