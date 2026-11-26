"""Viajes, posiciones del bus (HU-05, HU-06) y avisos «Voy a subir» (HU-07)."""
from django.conf import settings
from django.db import models
from django.db.models import Q


class Viaje(models.Model):
    class Estado(models.TextChoices):
        PROGRAMADO = "programado", "Programado"
        EN_CURSO = "en_curso", "En curso"
        TERMINADO = "terminado", "Terminado"
        CANCELADO = "cancelado", "Cancelado"

    ruta = models.ForeignKey("rutas.Ruta", related_name="viajes", on_delete=models.PROTECT)
    horario = models.ForeignKey("rutas.Horario", related_name="viajes", on_delete=models.PROTECT)
    fecha = models.DateField()
    chofer = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="viajes", on_delete=models.PROTECT
    )
    estado = models.CharField(
        max_length=12, choices=Estado.choices, default=Estado.PROGRAMADO
    )
    iniciado_en = models.DateTimeField(null=True, blank=True)
    terminado_en = models.DateTimeField(null=True, blank=True)
    ultima_latitud = models.FloatField(null=True, blank=True)
    ultima_longitud = models.FloatField(null=True, blank=True)
    ultima_posicion_en = models.DateTimeField(null=True, blank=True)
    paradas_registradas = models.ManyToManyField(
        "rutas.Parada", related_name="viajes_registrados", blank=True
    )

    class Meta:
        ordering = ["-fecha", "horario__salida", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["chofer"],
                condition=Q(estado="en_curso"),
                name="un_viaje_en_curso_por_chofer",
            )
        ]

    def __str__(self):
        return f"{self.ruta} · {self.fecha} {self.horario.salida:%H:%M}"


class PosicionDeViaje(models.Model):
    """Una posición recibida; el identificador del celular hace idempotente el reenvío."""

    viaje = models.ForeignKey(Viaje, related_name="posiciones", on_delete=models.CASCADE)
    id_cliente = models.CharField(max_length=64)
    latitud = models.FloatField()
    longitud = models.FloatField()
    tomada_en = models.DateTimeField()
    recibida_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["tomada_en", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["viaje", "id_cliente"], name="posicion_de_viaje_unica"
            )
        ]


class AvisoDeSubida(models.Model):
    """«Voy a subir»: un estudiante avisa en qué parada de un viaje va a subir (BUS-RF-09).

    Mientras está confirmado puede compartir su ubicación; solo se guarda la última,
    y se borra al subir, al cancelar, al cerrarse como «no se presentó» o al terminar
    el viaje (BUS-RF-08).
    """

    class Estado(models.TextChoices):
        CONFIRMADO = "confirmado", "Confirmado"
        A_BORDO = "a_bordo", "A bordo"
        CANCELADO = "cancelado", "Cancelado"
        NO_SE_PRESENTO = "no_se_presento", "No se presentó"

    ACTIVOS = (Estado.CONFIRMADO, Estado.A_BORDO)

    viaje = models.ForeignKey(Viaje, related_name="avisos", on_delete=models.CASCADE)
    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="avisos_de_subida", on_delete=models.PROTECT
    )
    parada = models.ForeignKey("rutas.Parada", related_name="avisos", on_delete=models.PROTECT)
    estado = models.CharField(max_length=16, choices=Estado.choices, default=Estado.CONFIRMADO)
    creado_en = models.DateTimeField(auto_now_add=True)
    cerrado_en = models.DateTimeField(null=True, blank=True)
    ubicacion_latitud = models.FloatField(null=True, blank=True)
    ubicacion_longitud = models.FloatField(null=True, blank=True)
    ubicacion_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["parada__orden", "creado_en", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["viaje", "estudiante"],
                condition=Q(estado__in=["confirmado", "a_bordo"]),
                name="un_aviso_activo_por_viaje",
            )
        ]

    def __str__(self):
        return f"{self.estudiante} · {self.parada} · {self.get_estado_display()}"
