"""Handler for summarized job completion notifications."""

from __future__ import annotations

from typing import Any

from .base import BaseEventHandler, EventContext


class JobFinishedSummaryHandler(BaseEventHandler):
    event_type = "job_finished_summary"
    required_fields = ("job_instance_id", "summary")

    def process(self, payload: dict[str, Any], context: EventContext) -> dict[str, Any]:
        summary = payload["summary"]

        return {
            "action": "job_summary_persisted",
            "total_items": summary.get("total_items", 0),
            "successful_items": summary.get("successful_items", 0),
            "failed_items": summary.get("failed_items", 0),
            "warnings": summary.get("warnings", []),
        }
