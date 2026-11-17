from enum import StrEnum


class Topic(StrEnum):
    METRICS = "telemetry.metrics.v1"
    LOGS = "telemetry.logs.v1"
    EVENTS = "telemetry.events.v1"
    ANOMALIES = "analysis.anomalies.v1"
    INCIDENTS = "analysis.incidents.v1"
    DEAD_LETTER = "system.dead-letter.v1"
