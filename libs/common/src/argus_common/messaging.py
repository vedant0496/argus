from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Protocol

from pydantic import BaseModel

from argus_common.topics import Topic


@dataclass(frozen=True, slots=True)
class Message:
    topic: str
    key: bytes | None
    value: bytes


def encode(model: BaseModel) -> bytes:
    return model.model_dump_json().encode()


class Publisher(Protocol):
    async def start(self) -> None: ...

    async def stop(self) -> None: ...

    async def publish_batch(
        self, topic: Topic, items: Iterable[tuple[str | None, BaseModel]]
    ) -> int:
        """Publish (key, model) pairs and return how many were acknowledged."""
        ...


@dataclass
class InMemoryBroker:
    """Process-local broker used in tests and for running services without Kafka."""

    topics: dict[str, list[Message]] = field(default_factory=lambda: defaultdict(list))

    async def start(self) -> None:
        return None

    async def stop(self) -> None:
        return None

    async def publish_batch(
        self, topic: Topic, items: Iterable[tuple[str | None, BaseModel]]
    ) -> int:
        count = 0
        for key, model in items:
            self.topics[topic].append(
                Message(topic=topic, key=key.encode() if key else None, value=encode(model))
            )
            count += 1
        return count

    def messages(self, topic: Topic) -> list[Message]:
        return list(self.topics.get(topic, []))
