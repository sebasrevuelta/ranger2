"""Flask application factory for jobinstance_events."""

from __future__ import annotations

import logging
import os
from typing import Any

from flask import Flask, jsonify, request
from flask_restx import Api, Resource

from .handlers import HANDLERS
from .handlers.base import EventContext, UnsupportedEventError

LOG = logging.getLogger(__name__)


def create_app(config: dict[str, Any] | None = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.update(
        SERVICE_NAME=os.getenv("SERVICE_NAME", "jobinstance_events"),
        JSON_SORT_KEYS=False,
        PUBSUB_TOPIC=os.getenv("PUBSUB_TOPIC", "jobinstance-events"),
    )
    if config:
        app.config.update(config)

    api = Api(
        app,
        title="jobinstance_events",
        version="0.1.0",
        description="Receives and processes job instance lifecycle/reporting events.",
    )

    @app.get("/healthz")
    def healthz():
        return jsonify(status="ok", service=app.config["SERVICE_NAME"])

    @app.get("/readyz")
    def readyz():
        return jsonify(status="ready", handlers=sorted(HANDLERS.keys()))

    @api.route("/api/v1/events")
    class EventsResource(Resource):
        def post(self):
            payload = request.get_json(silent=True) or {}
            event_type = payload.get("event_type")
            correlation_id = request.headers.get("X-Correlation-ID")

            if not event_type:
                return {"error": "event_type is required"}, 400

            handler = HANDLERS.get(event_type)
            if handler is None:
                raise UnsupportedEventError(f"Unsupported event_type: {event_type}")

            context = EventContext(
                correlation_id=correlation_id,
                source=request.headers.get("X-Event-Source", "unknown"),
            )
            result = handler().handle(payload, context)
            return result, 202

    @app.errorhandler(UnsupportedEventError)
    def unsupported_event(error: UnsupportedEventError):
        return jsonify(error=str(error)), 400

    @app.errorhandler(Exception)
    def unhandled_exception(error: Exception):
        LOG.exception("Unhandled jobinstance_events error")
        return jsonify(error="internal_server_error"), 500

    return app


app = create_app()
