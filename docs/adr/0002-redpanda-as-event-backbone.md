# ADR 0002: Redpanda (Kafka API) as the event backbone

- **Status:** accepted
- **Date:** 2026-11-17

## Context

Telemetry arrives in bursts and must fan out to several consumers (detection, storage, agent). Consumers need replay and per-key ordering.

## Options

| | Kafka API (Redpanda) | Redis Streams | NATS JetStream |
|---|---|---|---|
| Per-key ordering at scale | partitions | single stream per key | subjects |
| Replay / retention | days, cheap | memory-bound | yes |
| Ecosystem (connectors, tooling) | huge | small | medium |
| Local dev footprint | single binary, no ZooKeeper/JVM | tiny | tiny |

## Decision

Use the Kafka protocol, run with Redpanda locally and in CI. Production can use any Kafka-compatible service (MSK, Confluent, Redpanda Cloud) without code changes.

## Consequences

- Services depend on `aiokafka` only behind the `Publisher`/`Consumer` protocols in `argus_common.messaging`.
- Partition counts are a scaling ceiling for consumers. They are set generously up front (see `deploy/redpanda/create-topics.sh`).
