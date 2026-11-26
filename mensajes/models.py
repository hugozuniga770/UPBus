"""Modelos del chat directo (HU-14) y del chat de la ruta (HU-15)."""
from django.conf import settings
from django.db import models
from django.db.models import Q


class MiembroDeRuta(models.Model):
    """La ruta que una persona eligió para participar en su chat."""

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="rutas_elegidas",
        on_delete=models.CASCADE,
    )
    ruta = models.ForeignKey(
        "rutas.Ruta",
        related_name="miembros_del_chat",
        on_delete=models.CASCADE,
    )
    elegido_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["ruta__nombre", "usuario__nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "ruta"], name="miembro_unico_de_ruta"
            )
        ]

    def __str__(self):
        return f"{self.usuario} · {self.ruta}"


class Mensaje(models.Model):
    """Mensaje de texto de un chat directo o del chat de una ruta.

    En un chat directo, ``estudiante`` identifica la conversación privada del
    viaje. En un chat de ruta solo se llena ``ruta``. ``id_cliente`` hace
    idempotente un reenvío cuando el celular recupera la señal.
    """

    id_cliente = models.CharField(max_length=64, unique=True)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="mensajes_enviados",
        on_delete=models.PROTECT,
    )
    viaje = models.ForeignKey(
        "viajes.Viaje",
        null=True,
        blank=True,
        related_name="mensajes_directos",
        on_delete=models.CASCADE,
    )
    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="mensajes_directos",
        on_delete=models.PROTECT,
    )
    ruta = models.ForeignKey(
        "rutas.Ruta",
        null=True,
        blank=True,
        related_name="mensajes_del_chat",
        on_delete=models.CASCADE,
    )
    texto = models.CharField(max_length=1000)
    enviado_en = models.DateTimeField()

    class Meta:
        ordering = ["enviado_en", "id"]
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(viaje__isnull=False, estudiante__isnull=False, ruta__isnull=True)
                    | Q(viaje__isnull=True, estudiante__isnull=True, ruta__isnull=False)
                ),
                name="mensaje_directo_o_de_ruta",
            )
        ]

    def __str__(self):
        destino = self.viaje or self.ruta
        return f"{self.autor.nombre}: {self.texto[:40]} · {destino}"
