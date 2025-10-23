# WhatsApp Chatbot (Twilio + Flask)

Este ejemplo muestra cómo crear un chatbot sencillo para WhatsApp usando [Twilio's WhatsApp API](https://www.twilio.com/whatsapp). La aplicación está escrita en Python usando Flask y responde a mensajes entrantes con respuestas basadas en palabras clave.

> ⚠️ Necesitas una cuenta de Twilio con el sandbox de WhatsApp (o el WhatsApp Business API) configurado para poder utilizar este código. No compartas tus credenciales en repositorios públicos.

## Requisitos previos

1. **Python 3.9+** instalado en tu máquina.
2. Una cuenta de [Twilio](https://www.twilio.com/try-twilio) con el sandbox de WhatsApp habilitado.
3. Variables de entorno para tu `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` y `WHATSAPP_NUMBER` (número del remitente en formato `whatsapp:+14155238886` para el sandbox).

## Instalación

1. Crea y activa un entorno virtual:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Copia el archivo `config.example.env` a `.env` y completa las variables con tus credenciales reales:

   ```bash
   cp config.example.env .env
   ```

## Ejecución

1. Exporta las variables de entorno (o usa un gestor como `python-dotenv`):

   ```bash
   export $(grep -v '^#' .env | xargs)
   ```

2. Inicia la aplicación Flask:

   ```bash
   flask --app app run --host=0.0.0.0 --port=5000
   ```

3. Configura el webhook en la consola de Twilio para apuntar a `https://TU_DOMINIO/public/whatsapp/webhook`. Durante el desarrollo puedes usar [ngrok](https://ngrok.com/) para exponer tu servidor local.

## Personalización del bot

El bot define reglas básicas en `app.py` dentro de la función `build_response`. Puedes modificar la lógica para integrar servicios externos (por ejemplo, OpenAI, Dialogflow o bases de datos) y generar respuestas más complejas.

## Pruebas

Ejecuta los tests unitarios con `pytest` (la dependencia ya está incluida en `requirements.txt`):

```bash
pytest
```

## Pruebas rápidas

Envía un mensaje desde el número que hayas activado en el sandbox de Twilio al número de WhatsApp del sandbox (por lo general `+1 415 523 8886`). Deberías recibir una respuesta automática basada en la palabra clave que envíes.

## Despliegue

Para producción se recomienda ejecutar la app con un servidor WSGI como Gunicorn o desplegarla en una plataforma serverless (por ejemplo, AWS Lambda usando [Zappa](https://github.com/Miserlou/Zappa) o [Twilio Functions](https://www.twilio.com/en-us/functions)).

## Archivo de ejemplo `.env`

```env
TWILIO_ACCOUNT_SID=ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
TWILIO_AUTH_TOKEN=your_auth_token
WHATSAPP_NUMBER=whatsapp:+14155238886
DEFAULT_REPLY=Hola, soy un bot de ejemplo.
``` 

> Recuerda proteger tus credenciales y no subir el archivo `.env` al repositorio.
