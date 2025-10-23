# Automatización de procesos

Este repositorio contiene ejemplos orientados a la automatización de tareas en distintos contextos. Además de los cuadernos de demostración originales, se incluye ahora un ejemplo completo para administrar un salón de belleza mediante una API REST construida con Flask.

## Contenido destacado

- `salon_automation/`: módulo listo para usarse en la gestión de un salón de belleza. Permite registrar servicios, definir estilistas con sus horarios y agendar citas verificando disponibilidad.
- `whatsapp_bot/`: ejemplo de chatbot para WhatsApp utilizando Twilio y Flask.
- `tests/`: suite de pruebas automatizadas para validar la lógica de negocio.

## Requisitos

Se recomienda crear un entorno virtual con Python 3.9+ e instalar las dependencias según las necesidades de cada módulo (`salon_automation/requirements.txt`, `whatsapp_bot/requirements.txt`).

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r salon_automation/requirements.txt
```

## Ejecutar las pruebas

La suite de pruebas se puede ejecutar con:

```bash
pytest
```

## Próximos pasos sugeridos

- Integrar persistencia con una base de datos para guardar los registros del salón.
- Añadir una interfaz web o móvil para el personal del negocio.
- Conectar el chatbot de WhatsApp con la agenda del salón para confirmar citas automáticamente.
