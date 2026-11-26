# Guía de despliegue en Render

- Proyecto: UPBus — Buses UPB en tiempo real (UPB Santa Cruz)
- Responsable: Sebastian Cruz
- Fecha: 25/11/2026 · Tarea T22 · Issue [#17](https://github.com/hugozuniga770/UPBus/issues/17)
- Estado: configuración preparada; falta publicar cuando este cambio entre a `develop`

## 1. Decisión

UPBus se publica como un **Web Service gratuito de Render** construido con Docker y una base **Render Postgres gratuita**. El servicio web expone HTTPS, HTTP y WebSocket por el mismo dominio. Corre una sola instancia y un solo proceso Daphne, por eso la capa en memoria de Django Channels es suficiente para el MVP.

La interfaz React se compila dentro de la imagen. Django entrega su `index.html`, WhiteNoise entrega los recursos de `/static/` y Daphne sirve HTTP y WebSocket. El contenedor ejecuta las migraciones y `cargar_rutas` antes de arrancar.

Fuentes oficiales: [Web Services](https://render.com/docs/web-services), [WebSockets](https://render.com/docs/websocket), [desplegar Django](https://render.com/docs/deploy-django) y [Blueprints](https://render.com/docs/blueprint-spec).

## 2. Límites del plan gratuito

- El servicio se suspende después de 15 minutos sin tráfico y la primera visita puede tardar mientras vuelve a arrancar. Las solicitudes HTTP y los mensajes entrantes de conexiones WebSocket cuentan como tráfico.
- El disco del contenedor es efímero. Por eso los usuarios, viajes y mensajes van en PostgreSQL, no en el archivo SQLite del contenedor.
- La base PostgreSQL gratuita vence a los 30 días. Para la demostración se debe crear o renovar cerca de la fecha de uso y conservar un respaldo si hace falta.
- El padrón real nunca se incluye en la imagen ni en Git. Se carga con la opción **Secret File** de Render.

Los detalles vigentes del plan están en [Free Deploys](https://render.com/docs/free) y la carga segura del padrón en [Environment Variables and Secrets](https://render.com/docs/configure-environment-variables).

## 3. Publicar desde `develop`

1. Integra el Pull Request de T22 en `develop`. No publiques desde `main` ni subas cambios directos a `develop`.
2. En Render, elige **New > Blueprint** y conecta `hugozuniga770/UPBus`.
3. Selecciona la rama `develop`. Render leerá `render.yaml` y propondrá `upbus-santa-cruz` y `upbus-db`, ambos con plan gratuito.
4. Antes de desplegar, revisa que `UPBUS_DEBUG` sea `0`, que `UPBUS_SECRET_KEY` tenga un valor generado y que `DATABASE_URL` venga de `upbus-db`.
5. En el servicio web, abre **Environment > Secret Files** y crea un archivo llamado `padron.local.json`; Render lo expondrá como `/etc/secrets/padron.local.json`. Pega como contenido el archivo generado con `importar_padron`; no lo copies a una variable visible ni al repositorio.
6. Confirma que `UPBUS_PADRON` valga `/etc/secrets/padron.local.json` y ejecuta el despliegue.

El comando de arranque hace, en orden:

```text
python manage.py migrate
python manage.py cargar_rutas
daphne -b 0.0.0.0 -p $PORT config.asgi:application
```

## 4. Comprobación

Cuando Render indique **Live**:

1. Abre la URL `https://upbus-santa-cruz.onrender.com` que muestre Render. Debe redirigir siempre a HTTPS y cargar la interfaz.
2. Registra una cuenta que exista en el archivo secreto. Un código del padrón de ejemplo no tiene por qué funcionar en este entorno.
3. Inicia sesión y abre una ruta. Confirma en las herramientas del navegador que `/api/...` responde por HTTPS.
4. Con dos navegadores o celulares, inicia un viaje y comprueba que la ubicación llegue por `wss://.../ws/viajes/<id>/`.
5. Reinicia o vuelve a desplegar el servicio y comprueba que la cuenta siga en la base PostgreSQL.

Si la primera visita devuelve temporalmente 502, espera a que el evento de despliegue indique **Live** y revisa sus logs. Un error permanente antes de Daphne suele indicar una migración, una variable o el archivo secreto faltante.

## 5. Actualizar

Los cambios futuros entran a `develop` por Pull Request. Al actualizar esa rama, Render reconstruye el contenedor y ejecuta las migraciones. El padrón permanece como secreto del servicio y la base permanece separada del contenedor.

Antes de la demostración, revisa la fecha de vencimiento de PostgreSQL y ejecuta las comprobaciones de la sección 4.

## 6. Participación y asistencia utilizada

- **Sebastian Cruz:** responsable de T22, de la elección del hosting y de la publicación.
- **Asistencia de IA:** Sebastian usó OpenAI Codex para consultar la documentación oficial de Render, preparar la configuración, las pruebas y esta guía.
