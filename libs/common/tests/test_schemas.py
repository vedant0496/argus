from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from argus_common.schemas import MetricPoint, Resource


def make_point(**overrides: object) -> MetricPoint:
    data: dict[str, object] = {
        "tenant_id": "acme",
        "name": "http.server.latency_p99",
        "value": 120.5,
        "timestamp": datetime(2026, 11, 17, tzinfo=UTC),
        "labels": {"route": "/checkout", "method": "POST"},
        "resource": Resource(service="checkout", host="node-1"),
    }
    data.update(overrides)
    return MetricPoint.model_validate(data)


def test_series_key_is_independent_of_label_order() -> None:
    a = make_point(labels={"route": "/checkout", "method": "POST"})
    b = make_point(labels={"method": "POST", "route": "/checkout"})
    assert a.series_key == b.series_key


def test_series_key_differs_per_host() -> None:
    a = make_point(resource=Resource(service="checkout", host="node-1"))
    b = make_point(resource=Resource(service="checkout", host="node-2"))
    assert a.series_key != b.series_key


@pytest.mark.parametrize(
    "overrides",
    [
        {"timestamp": datetime(2026, 11, 17)},
        {"value": float("nan")},
        {"value": float("inf")},
        {"tenant_id": "Acme Corp"},
        {"name": "1-invalid"},
    ],
    ids=["naive-timestamp", "nan", "inf", "bad-tenant", "bad-metric-name"],
)
def test_rejects_invalid_points(overrides: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        make_point(**overrides)


def test_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        make_point(unexpected="field")
