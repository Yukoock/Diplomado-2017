"""Aplicación Flask para un chatbot básico de WhatsApp usando Twilio."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict

from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

load_dotenv()


@dataclass
class BotConfig:
    """Estructura de configuración del bot."""

    account_sid: str
    auth_token: str
    whatsapp_number: str
    default_reply: str = "Hola, soy un bot de ejemplo."

    @classmethod
    def from_env(cls) -> "BotConfig":
        try:
            return cls(
                account_sid=os.environ["TWILIO_ACCOUNT_SID"],
                auth_token=os.environ["TWILIO_AUTH_TOKEN"],
                whatsapp_number=os.environ["WHATSAPP_NUMBER"],
                default_reply=os.environ.get("DEFAULT_REPLY", "Hola, soy un bot de ejemplo."),
            )
        except KeyError as exc:
            missing = ", ".join(key for key in ("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "WHATSAPP_NUMBER") if key not in os.environ)
            raise RuntimeError(
                "Faltan variables de entorno requeridas: " + missing
            ) from exc


KEYWORD_RESPONSES: Dict[str, str] = {
    "hola": "¡Hola! ¿En qué puedo ayudarte hoy?",
    "menu": "Opciones disponibles: \n1. Horarios\n2. Promociones\n3. Hablar con agente",
    "horarios": "Nuestro horario de atención es de lunes a viernes de 9 a 18 h.",
    "promociones": "Visita https://midominio.com/promociones para ver las ofertas actuales.",
    "agente": "Un agente humano se pondrá en contacto contigo pronto.",
}


def create_app() -> Flask:
    """Crea y configura la aplicación Flask."""

    config = BotConfig.from_env()
    app = Flask(__name__)

    @app.post("/public/whatsapp/webhook")
    def whatsapp_webhook() -> str:
        """Endpoint que procesa mensajes entrantes desde Twilio."""

        incoming_msg = request.form.get("Body", "").strip().lower()
        response = MessagingResponse()
        message = response.message()

        reply = build_response(incoming_msg, KEYWORD_RESPONSES, config.default_reply)
        message.body(reply)
        message.from_(config.whatsapp_number)

        return str(response)

    @app.get("/health")
    def healthcheck() -> Dict[str, str]:
        """Endpoint de verificación de salud."""

        return {"status": "ok"}

    return app


def build_response(incoming_msg: str, keyword_responses: Dict[str, str], default_reply: str) -> str:
    """Determina la respuesta del bot a partir del mensaje entrante."""

    for keyword, reply in keyword_responses.items():
        if incoming_msg.startswith(keyword):
            return reply
    return default_reply


app = create_app()
