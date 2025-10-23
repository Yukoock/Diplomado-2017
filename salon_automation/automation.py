"""Lógica principal para automatizar la operación de un salón de belleza."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time, timedelta
from typing import Dict, Iterable, List, Optional
import uuid


class SalonError(Exception):
    """Error base para la automatización del salón."""


@dataclass(frozen=True)
class Service:
    """Servicio ofrecido por el salón."""

    id: str
    name: str
    duration_minutes: int
    price: float

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "name": self.name,
            "duration_minutes": self.duration_minutes,
            "price": self.price,
        }


@dataclass(frozen=True)
class Stylist:
    """Estilista con habilidades y horario laboral."""

    id: str
    name: str
    skills: List[str]
    work_start: time
    work_end: time

    def can_perform(self, service_id: str) -> bool:
        return service_id in self.skills

    def works_during(self, start: datetime, end: datetime) -> bool:
        start_time = start.time()
        end_time = end.time()
        return self.work_start <= start_time and end_time <= self.work_end

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "name": self.name,
            "skills": list(self.skills),
            "work_start": self.work_start.strftime("%H:%M"),
            "work_end": self.work_end.strftime("%H:%M"),
        }


@dataclass
class Appointment:
    """Cita agendada en el salón."""

    id: str
    client_name: str
    client_phone: str
    service_id: str
    stylist_id: str
    start_time: datetime
    end_time: datetime

    def overlaps(self, other: "Appointment") -> bool:
        return not (self.end_time <= other.start_time or self.start_time >= other.end_time)

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "client_name": self.client_name,
            "client_phone": self.client_phone,
            "service_id": self.service_id,
            "stylist_id": self.stylist_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
        }


class InMemorySalonStore:
    """Repositorio en memoria para servicios, estilistas y citas."""

    def __init__(self) -> None:
        self.services: Dict[str, Service] = {}
        self.stylists: Dict[str, Stylist] = {}
        self.appointments: Dict[str, Appointment] = {}

    def add_service(self, service: Service) -> None:
        self.services[service.id] = service

    def add_stylist(self, stylist: Stylist) -> None:
        self.stylists[stylist.id] = stylist

    def add_appointment(self, appointment: Appointment) -> None:
        self.appointments[appointment.id] = appointment

    def remove_appointment(self, appointment_id: str) -> None:
        self.appointments.pop(appointment_id, None)

    def get_service(self, service_id: str) -> Optional[Service]:
        return self.services.get(service_id)

    def get_stylist(self, stylist_id: str) -> Optional[Stylist]:
        return self.stylists.get(stylist_id)

    def get_appointment(self, appointment_id: str) -> Optional[Appointment]:
        return self.appointments.get(appointment_id)

    def iter_appointments_for_stylist(self, stylist_id: str) -> Iterable[Appointment]:
        return (appt for appt in self.appointments.values() if appt.stylist_id == stylist_id)

    def iter_appointments_on_date(self, target_date: datetime) -> Iterable[Appointment]:
        return (
            appt
            for appt in self.appointments.values()
            if appt.start_time.date() == target_date.date()
        )


class SalonAutomation:
    """Gestor principal para la automatización del salón."""

    def __init__(self, store: Optional[InMemorySalonStore] = None) -> None:
        self.store = store or InMemorySalonStore()

    @staticmethod
    def _new_id() -> str:
        return uuid.uuid4().hex

    def register_service(self, name: str, duration_minutes: int, price: float) -> Service:
        if duration_minutes <= 0:
            raise SalonError("La duración del servicio debe ser mayor a 0 minutos.")
        if price < 0:
            raise SalonError("El precio no puede ser negativo.")
        service = Service(id=self._new_id(), name=name, duration_minutes=duration_minutes, price=price)
        self.store.add_service(service)
        return service

    def register_stylist(self, name: str, skills: List[str], work_start: time, work_end: time) -> Stylist:
        if work_end <= work_start:
            raise SalonError("El horario de fin debe ser posterior al horario de inicio.")
        stylist = Stylist(id=self._new_id(), name=name, skills=list(skills), work_start=work_start, work_end=work_end)
        self.store.add_stylist(stylist)
        return stylist

    def schedule_appointment(
        self,
        client_name: str,
        client_phone: str,
        service_id: str,
        stylist_id: str,
        start_time: datetime,
    ) -> Appointment:
        service = self.store.get_service(service_id)
        if not service:
            raise SalonError("Servicio no encontrado.")
        stylist = self.store.get_stylist(stylist_id)
        if not stylist:
            raise SalonError("Estilista no encontrado.")
        if not stylist.can_perform(service_id):
            raise SalonError("El estilista seleccionado no ofrece el servicio solicitado.")

        end_time = start_time + timedelta(minutes=service.duration_minutes)
        if not stylist.works_during(start_time, end_time):
            raise SalonError("La cita está fuera del horario laboral del estilista.")

        proposed = Appointment(
            id="temp",
            client_name=client_name,
            client_phone=client_phone,
            service_id=service_id,
            stylist_id=stylist_id,
            start_time=start_time,
            end_time=end_time,
        )

        for existing in self.store.iter_appointments_for_stylist(stylist_id):
            if existing.overlaps(proposed):
                raise SalonError("El estilista ya tiene una cita programada en ese horario.")

        appointment = Appointment(
            id=self._new_id(),
            client_name=client_name,
            client_phone=client_phone,
            service_id=service_id,
            stylist_id=stylist_id,
            start_time=start_time,
            end_time=end_time,
        )
        self.store.add_appointment(appointment)
        return appointment

    def cancel_appointment(self, appointment_id: str) -> bool:
        if self.store.get_appointment(appointment_id):
            self.store.remove_appointment(appointment_id)
            return True
        return False

    def daily_agenda(self, date: datetime) -> List[Dict[str, object]]:
        agenda = [appt.to_dict() for appt in sorted(self.store.iter_appointments_on_date(date), key=lambda a: a.start_time)]
        return agenda

    def generate_reminder(self, appointment_id: str) -> str:
        appointment = self.store.get_appointment(appointment_id)
        if not appointment:
            raise SalonError("Cita no encontrada.")
        service = self.store.get_service(appointment.service_id)
        stylist = self.store.get_stylist(appointment.stylist_id)
        if not service or not stylist:
            raise SalonError("Información incompleta para generar el recordatorio.")
        start_str = appointment.start_time.strftime("%d/%m/%Y %H:%M")
        return (
            f"Hola {appointment.client_name}, te recordamos tu cita de {service.name} "
            f"con {stylist.name} el {start_str}."
        )

    def list_services(self) -> List[Dict[str, object]]:
        return [service.to_dict() for service in self.store.services.values()]

    def list_stylists(self) -> List[Dict[str, object]]:
        return [stylist.to_dict() for stylist in self.store.stylists.values()]

    def list_appointments(self) -> List[Dict[str, object]]:
        return [appt.to_dict() for appt in self.store.appointments.values()]
