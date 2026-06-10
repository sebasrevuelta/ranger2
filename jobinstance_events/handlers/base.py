"""Base abstractions for job instance event handlers."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

LOG = logging.getLogger(__name__)


class UnsupportedEventError(ValueError):
    """Raised when an event type is not registered."""


class EventValidationError(ValueError):
    """Raised when an event payload is missing required data."""


@dataclass(frozen=True)
class EventContext:
    correlation_id: str | None = None
    source: str = "unknown"


class BaseEventHandler:
    """Base handler with shared validation and response helpers."""

    event_type: str = "unknown"
    required_fields: tuple[str, ...] = ("job_instance_id",)

    def validate(self, payload: dict[str, Any]) -> None:
        missing = [field for field in self.required_fields if field not in payload]
        if missing:
            raise EventValidationError(
                f"Missing required fields for {self.event_type}: {', '.join(missing)}"
            )

    def handle(self, payload: dict[str, Any], context: EventContext) -> dict[str, Any]:
        self.validate(payload)
        LOG.info(
            "Processing event",
            extra={
                "event_type": self.event_type,
                "job_instance_id": payload.get("job_instance_id"),
                "correlation_id": context.correlation_id,
                "source": context.source,
            },
        )
        details = self.process(payload, context)
        return {
            "status": "accepted",
            "event_type": self.event_type,
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "details": details,
        }

    def process(self, payload: dict[str, Any], context: EventContext) -> dict[str, Any]:
        """Process a validated payload.

        Subclasses should override this method and return serializable metadata.
        """
        return {}
