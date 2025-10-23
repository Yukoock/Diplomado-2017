"""Pruebas para la automatización del salón de belleza."""
from __future__ import annotations

from datetime import datetime, time
import pathlib
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from salon_automation.automation import SalonAutomation, SalonError


def create_basic_setup():
    automation = SalonAutomation()
    service = automation.register_service("Corte de cabello", 30, 12.5)
    stylist = automation.register_stylist(
        name="Mariana",
        skills=[service.id],
        work_start=time(9, 0),
        work_end=time(18, 0),
    )
    return automation, service, stylist


def test_schedule_appointment_creates_entry_and_reminder():
    automation, service, stylist = create_basic_setup()
    appointment = automation.schedule_appointment(
        client_name="Ana",
        client_phone="5551234567",
        service_id=service.id,
        stylist_id=stylist.id,
        start_time=datetime(2024, 6, 1, 10, 0),
    )

    assert appointment.end_time == datetime(2024, 6, 1, 10, 30)
    reminder = automation.generate_reminder(appointment.id)
    assert "Ana" in reminder
    assert service.name in reminder
    assert stylist.name in reminder


def test_prevent_overlapping_appointments():
    automation, service, stylist = create_basic_setup()
    automation.schedule_appointment(
        client_name="Ana",
        client_phone="5551234567",
        service_id=service.id,
        stylist_id=stylist.id,
        start_time=datetime(2024, 6, 1, 10, 0),
    )

    with pytest.raises(SalonError):
        automation.schedule_appointment(
            client_name="Bea",
            client_phone="5557654321",
            service_id=service.id,
            stylist_id=stylist.id,
            start_time=datetime(2024, 6, 1, 10, 15),
        )


def test_stylist_must_offer_service():
    automation = SalonAutomation()
    service_a = automation.register_service("Color", 90, 35.0)
    service_b = automation.register_service("Peinado", 30, 15.0)
    stylist = automation.register_stylist(
        name="Luis",
        skills=[service_a.id],
        work_start=time(10, 0),
        work_end=time(19, 0),
    )

    with pytest.raises(SalonError):
        automation.schedule_appointment(
            client_name="Camila",
            client_phone="5559876543",
            service_id=service_b.id,
            stylist_id=stylist.id,
            start_time=datetime(2024, 6, 1, 11, 0),
        )
