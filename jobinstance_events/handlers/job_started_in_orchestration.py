"""Handler for orchestration start events."""

from __future__ import annotations

from typing import Any

from .base import BaseEventHandler, EventContext


class JobStartedInOrchestrationHandler(BaseEventHandler):
    event_type = "job_started_in_orchestration"
    required_fields = ("job_instance_id", "orchestration_id")

    def process(self, payload: dict[str, Any], context: EventContext) -> dict[str, Any]:
        return {
            "action": "job_start_recorded",
            "orchestration_id": payload["orchestration_id"],
            "node_id": payload.get("node_id"),
            "pop_id": payload.get("pop_id"),
        }
