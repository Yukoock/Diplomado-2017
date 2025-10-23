"""API REST para la automatización de un salón de belleza."""
from __future__ import annotations

from datetime import datetime, time
from typing import Any, Dict

from flask import Flask, jsonify, request

from .automation import SalonAutomation, SalonError


def parse_time(value: str) -> time:
    try:
        return datetime.strptime(value, "%H:%M").time()
    except ValueError as exc:
        raise SalonError("El formato de hora debe ser HH:MM.") from exc


def parse_datetime(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise SalonError("El formato de fecha debe ser ISO 8601, por ejemplo 2024-05-01T10:00.") from exc


def create_app(automation: SalonAutomation | None = None) -> Flask:
    automation = automation or SalonAutomation()
    app = Flask(__name__)

    @app.post("/services")
    def create_service() -> Any:
        payload: Dict[str, Any] = request.get_json(force=True)
        service = automation.register_service(
            name=payload["name"],
            duration_minutes=int(payload["duration_minutes"]),
            price=float(payload["price"]),
        )
        return jsonify(service.to_dict()), 201

    @app.get("/services")
    def list_services() -> Any:
        return jsonify(automation.list_services())

    @app.post("/stylists")
    def create_stylist() -> Any:
        payload: Dict[str, Any] = request.get_json(force=True)
        stylist = automation.register_stylist(
            name=payload["name"],
            skills=list(payload.get("skills", [])),
            work_start=parse_time(payload["work_start"]),
            work_end=parse_time(payload["work_end"]),
        )
        return jsonify(stylist.to_dict()), 201

    @app.get("/stylists")
    def list_stylists() -> Any:
        return jsonify(automation.list_stylists())

    @app.post("/appointments")
    def create_appointment() -> Any:
        payload: Dict[str, Any] = request.get_json(force=True)
        appointment = automation.schedule_appointment(
            client_name=payload["client_name"],
            client_phone=payload["client_phone"],
            service_id=payload["service_id"],
            stylist_id=payload["stylist_id"],
            start_time=parse_datetime(payload["start_time"]),
        )
        return jsonify(appointment.to_dict()), 201

    @app.get("/appointments")
    def list_appointments() -> Any:
        date_filter = request.args.get("date")
        if date_filter:
            agenda = automation.daily_agenda(parse_datetime(date_filter))
            return jsonify(agenda)
        return jsonify(automation.list_appointments())

    @app.delete("/appointments/<appointment_id>")
    def delete_appointment(appointment_id: str) -> Any:
        deleted = automation.cancel_appointment(appointment_id)
        status = 204 if deleted else 404
        return ("", status)

    @app.post("/appointments/<appointment_id>/reminder")
    def appointment_reminder(appointment_id: str) -> Any:
        reminder = automation.generate_reminder(appointment_id)
        return jsonify({"reminder": reminder})

    @app.errorhandler(SalonError)
    def handle_salon_error(error: SalonError):  # type: ignore[override]
        response = jsonify({"error": str(error)})
        response.status_code = 400
        return response

    return app


app = create_app()
