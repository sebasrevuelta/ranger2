"""Handler for job summary requests."""

from __future__ import annotations

from typing import Any

from .base import BaseEventHandler, EventContext


class JobSummaryRequestedHandler(BaseEventHandler):
    event_type = "job_summary_requested"
    required_fields = ("job_instance_id",)

    def process(self, payload: dict[str, Any], context: EventContext) -> dict[str, Any]:
        sections = payload.get("sections") or ["overview", "errors", "throughput"]

        return {
            "action": "job_summary_generation_requested",
            "sections": sections,
            "requester": payload.get("requested_by", "system"),
        }
