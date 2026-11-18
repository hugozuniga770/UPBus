"""El rechazo de una operación, con su causa (BUS-RC-01).

Las reglas lanzan `Rechazo` y la vista lo convierte en una respuesta JSON
`{"causa": "..."}` (ver `comun/respuestas.py`). Un rechazo nunca deja datos a
medias (BUS-RC-03): por eso los servicios que escriben usan transacciones.
"""


class Rechazo(Exception):
    """La operación no se permite. `causa` es el mensaje que ve la persona."""

    codigo_http = 400

    def __init__(self, causa, codigo_http=None):
        super().__init__(causa)
        self.causa = causa
        if codigo_http is not None:
            self.codigo_http = codigo_http


class SinPermiso(Rechazo):
    """El rol de la cuenta no permite la operación (BUS-RF-03)."""

    codigo_http = 403


class NoExiste(Rechazo):
    """Lo pedido no existe."""

    codigo_http = 404
