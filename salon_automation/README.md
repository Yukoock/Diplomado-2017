# Automatización para un salón de belleza

Este módulo ofrece una API REST sencilla para gestionar los servicios, estilistas y citas de un salón de belleza. Está construido con Flask y utiliza un almacenamiento en memoria pensado para demostraciones o prototipos.

## Características

- Registro de servicios con duración y precio.
- Registro de estilistas con habilidades y horario laboral.
- Agenda de citas con validaciones de disponibilidad y solapamiento.
- Generación de recordatorios personalizados para los clientes.
- Endpoint para consultar la agenda diaria.

## Requisitos

- Python 3.9+
- [Flask](https://flask.palletsprojects.com/)

Instala las dependencias dentro de un entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

El archivo `requirements.txt` de este directorio contiene Flask y pytest para ejecutar las pruebas.

## Uso rápido

1. Arranca la API:

   ```bash
   export FLASK_APP=salon_automation.api:app
   flask run --host=0.0.0.0 --port=5000
   ```

2. Registra un servicio:

   ```bash
   curl -X POST http://localhost:5000/services \
     -H "Content-Type: application/json" \
     -d '{"name": "Manicure", "duration_minutes": 45, "price": 18.0}'
   ```

3. Crea un estilista y agenda una cita usando los identificadores devueltos por la API.

4. Consulta la agenda del día:

   ```bash
   curl "http://localhost:5000/appointments?date=2024-06-01T00:00:00"
   ```

## Pruebas

Ejecuta la suite con:

```bash
pytest
```

## Próximos pasos sugeridos

- Sustituir el almacenamiento en memoria por una base de datos.
- Integrar recordatorios mediante correo electrónico, SMS o WhatsApp.
- Añadir autenticación y control de acceso para el personal del salón.
