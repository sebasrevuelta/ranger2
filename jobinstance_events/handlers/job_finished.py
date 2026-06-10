"""Handler for job_finished events."""

from __future__ import annotations

from typing import Any

from .base import BaseEventHandler, EventContext


class JobFinishedHandler(BaseEventHandler):
    event_type = "job_finished"
    required_fields = ("job_instance_id", "status")

    def process(self, payload: dict[str, Any], context: EventContext) -> dict[str, Any]:
        status = payload["status"]
        duration_seconds = payload.get("duration_seconds")
        counters = payload.get("counters", {})

        return {
            "action": "job_completion_recorded",
            "status": status,
            "duration_seconds": duration_seconds,
            "files_processed": counters.get("files_processed", 0),
            "errors": counters.get("errors", 0),
        }
