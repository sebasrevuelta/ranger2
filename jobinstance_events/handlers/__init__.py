"""Event handler registry."""

from .export_job_reports import ExportJobReportsHandler
from .job_finished import JobFinishedHandler
from .job_finished_summary import JobFinishedSummaryHandler
from .job_report_requested import JobReportRequestedHandler
from .job_started_in_orchestration import JobStartedInOrchestrationHandler
from .job_summary_requested import JobSummaryRequestedHandler

HANDLERS = {
    "export_job_reports": ExportJobReportsHandler,
    "job_finished": JobFinishedHandler,
    "job_finished_summary": JobFinishedSummaryHandler,
    "job_report_requested": JobReportRequestedHandler,
    "job_started_in_orchestration": JobStartedInOrchestrationHandler,
    "job_summary_requested": JobSummaryRequestedHandler,
}
