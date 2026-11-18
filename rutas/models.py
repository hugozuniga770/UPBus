"""Rutas, horarios, paradas y el modo registro (HU-04, HU-18)."""
from django.conf import settings
from django.db import models


class Ruta(models.Model):
    clave = models.SlugField(unique=True)
    nombre = models.CharField(max_length=60)
    punto_de_partida = models.CharField(max_length=150)
    activa = models.BooleanField(default=True)
    # Puntos [latitud, longitud] del recorrido, tomados del primer registro.
    recorrido = models.JSONField(default=list, blank=True)
    nota = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Horario(models.Model):
    class Sentido(models.TextChoices):
        INGRESO = "ingreso", "Ingreso a la U"
        SALIDA = "salida", "Salida de la U"

    ruta = models.ForeignKey(Ruta, related_name="horarios", on_delete=models.CASCADE)
    sentido = models.CharField(max_length=10, choices=Sentido.choices)
    salida = models.TimeField()
    llegada_limite = models.TimeField(null=True, blank=True)

    class Meta:
        ordering = ["sentido", "salida"]
        constraints = [
            models.UniqueConstraint(fields=["ruta", "sentido", "salida"], name="horario_unico")
        ]

    def __str__(self):
        return f"{self.ruta} · {self.get_sentido_display()} {self.salida:%H:%M}"


class Parada(models.Model):
    class Estado(models.TextChoices):
        APROBADA = "aprobada", "Aprobada"
        PROPUESTA = "propuesta", "Propuesta"
        RECHAZADA = "rechazada", "Rechazada"

    ruta = models.ForeignKey(Ruta, related_name="paradas", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=120)
    latitud = models.FloatField()
    longitud = models.FloatField()
    orden = models.PositiveIntegerField(default=0)
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.APROBADA)
    creada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["orden", "id"]

    def __str__(self):
        return f"{self.nombre} ({self.ruta})"

    @property
    def punto(self):
        return (self.latitud, self.longitud)


class RegistroDeRecorrido(models.Model):
    """Un recorrido hecho en modo registro (HU-18)."""

    class Estado(models.TextChoices):
        EN_CURSO = "en_curso", "En curso"
        TERMINADO = "terminado", "Terminado"
        CANCELADO = "cancelado", "Cancelado"

    # Identificador que genera el celular: un reenvío o una importación no duplica.
    id_cliente = models.CharField(max_length=64, unique=True, null=True, blank=True)
    ruta = models.ForeignKey(Ruta, related_name="registros", on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, null=True, blank=True, on_delete=models.SET_NULL)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.EN_CURSO)
    iniciado_en = models.DateTimeField()
    terminado_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-iniciado_en"]

    def __str__(self):
        return f"Registro {self.pk} · {self.ruta} · {self.get_estado_display()}"


class MarcaDeParada(models.Model):
    """Cada «Parada aquí» del modo registro."""

    registro = models.ForeignKey(RegistroDeRecorrido, related_name="marcas", on_delete=models.CASCADE)
    id_cliente = models.CharField(max_length=64)
    nombre = models.CharField(max_length=120, blank=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    precision_m = models.FloatField(null=True, blank=True)
    marcada_en = models.DateTimeField()
    recibida_en = models.DateTimeField(auto_now_add=True)
    parada = models.ForeignKey(Parada, null=True, blank=True, on_delete=models.SET_NULL)
    minutos_desde_salida = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ["marcada_en"]
        constraints = [
            models.UniqueConstraint(fields=["registro", "id_cliente"], name="marca_unica")
        ]

    @property
    def punto(self):
        return (self.latitud, self.longitud)


class PuntoDeRegistro(models.Model):
    """Posiciones del recorrido tomadas durante el modo registro."""

    registro = models.ForeignKey(RegistroDeRecorrido, related_name="puntos", on_delete=models.CASCADE)
    id_cliente = models.CharField(max_length=64)
    latitud = models.FloatField()
    longitud = models.FloatField()
    precision_m = models.FloatField(null=True, blank=True)
    tomado_en = models.DateTimeField()

    class Meta:
        ordering = ["tomado_en"]
        constraints = [
            models.UniqueConstraint(fields=["registro", "id_cliente"], name="punto_unico")
        ]


class PasoPorParada(models.Model):
    """Cada vez que el bus pasó por una parada: de aquí sale la hora aproximada (RF-11).

    Lo crean el modo registro y, más adelante, los viajes reales (HU-06).
    """

    parada = models.ForeignKey(Parada, related_name="pasos", on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, null=True, blank=True, on_delete=models.SET_NULL)
    registro = models.ForeignKey(
        RegistroDeRecorrido, null=True, blank=True, related_name="pasos", on_delete=models.CASCADE
    )
    minutos_desde_salida = models.FloatField()
    ocurrido_en = models.DateTimeField()
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-ocurrido_en", "-id"]
