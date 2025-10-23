"""Paquete para la automatización de un salón de belleza."""
from .automation import (
    Appointment,
    InMemorySalonStore,
    SalonAutomation,
    SalonError,
    Service,
    Stylist,
)

__all__ = [
    "Appointment",
    "InMemorySalonStore",
    "SalonAutomation",
    "SalonError",
    "Service",
    "Stylist",
    "create_app",
]


def create_app(*args, **kwargs):
    """Importa perezosamente la fábrica de la API para evitar dependencias innecesarias."""

    from .api import create_app as _create_app

    return _create_app(*args, **kwargs)
