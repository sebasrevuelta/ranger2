"""Handler for export_job_reports events."""

from __future__ import annotations

from typing import Any

from .base import BaseEventHandler, EventContext


class ExportJobReportsHandler(BaseEventHandler):
    event_type = "export_job_reports"
    required_fields = ("job_instance_id", "requested_by")

    def process(self, payload: dict[str, Any], context: EventContext) -> dict[str, Any]:
        report_types = payload.get("report_types") or ["overview", "transfer_statistics"]
        destination = payload.get("destination", "default-report-bucket")

        # In production this would enqueue report generation work.
        return {
            "action": "report_export_enqueued",
            "report_types": report_types,
            "destination": destination,
            "requested_by": payload["requested_by"],
        }
