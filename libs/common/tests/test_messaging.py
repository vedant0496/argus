from argus_common.messaging import InMemoryBroker
from argus_common.schemas import Resource
from argus_common.schemas.telemetry import Event, EventType
from argus_common.topics import Topic


async def test_in_memory_broker_round_trip() -> None:
    broker = InMemoryBroker()
    event = Event(
        tenant_id="acme",
        timestamp="2026-11-17T10:00:00Z",  # type: ignore[arg-type]
        type=EventType.DEPLOYMENT,
        title="checkout v2.3.1 rolled out",
        resource=Resource(service="checkout"),
    )

    acked = await broker.publish_batch(Topic.EVENTS, [("checkout", event)])

    [message] = broker.messages(Topic.EVENTS)
    assert acked == 1
    assert message.key == b"checkout"
    assert Event.model_validate_json(message.value) == event
