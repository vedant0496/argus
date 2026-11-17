#!/usr/bin/env bash
set -euo pipefail

BROKERS="${BROKERS:-redpanda:9092}"

create() {
  local topic=$1 partitions=$2 retention_ms=$3
  rpk topic create "$topic" -X brokers="$BROKERS" -p "$partitions" -r 1 \
    -c retention.ms="$retention_ms" -c compression.type=zstd 2>&1 \
    | grep -v "TOPIC_ALREADY_EXISTS" || true
}

DAY=$((24 * 60 * 60 * 1000))

create telemetry.metrics.v1   12 $((3 * DAY))
create telemetry.logs.v1      12 $((3 * DAY))
create telemetry.events.v1     6 $((7 * DAY))
create analysis.anomalies.v1   6 $((14 * DAY))
create analysis.incidents.v1   3 $((30 * DAY))
create system.dead-letter.v1   3 $((14 * DAY))

rpk topic list -X brokers="$BROKERS"
