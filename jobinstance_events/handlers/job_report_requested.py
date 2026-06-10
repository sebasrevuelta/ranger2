"""Handler for ad-hoc job report requests."""

from __future__ import annotations

from typing import Any

from .base import BaseEventHandler, EventContext


class JobReportRequestedHandler(BaseEventHandler):
    event_type = "job_report_requested"
    required_fields = ("job_instance_id", "report_name")

    def process(self, payload: dict[str, Any], context: EventContext) -> dict[str, Any]:
        report_name = payload["report_name"]
        output_format = payload.get("format", "csv")

        return {
            "action": "job_report_generation_requested",
            "report_name": report_name,
            "format": output_format,
            "include_raw_data": bool(payload.get("include_raw_data", False)),
        }
