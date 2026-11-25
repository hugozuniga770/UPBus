# Generated for HU-05 and HU-06.
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("rutas", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Viaje",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fecha", models.DateField()),
                ("estado", models.CharField(choices=[("programado", "Programado"), ("en_curso", "En curso"), ("terminado", "Terminado"), ("cancelado", "Cancelado")], default="programado", max_length=12)),
                ("iniciado_en", models.DateTimeField(blank=True, null=True)),
                ("terminado_en", models.DateTimeField(blank=True, null=True)),
                ("ultima_latitud", models.FloatField(blank=True, null=True)),
                ("ultima_longitud", models.FloatField(blank=True, null=True)),
                ("ultima_posicion_en", models.DateTimeField(blank=True, null=True)),
                ("chofer", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="viajes", to=settings.AUTH_USER_MODEL)),
                ("horario", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="viajes", to="rutas.horario")),
                ("paradas_registradas", models.ManyToManyField(blank=True, related_name="viajes_registrados", to="rutas.parada")),
                ("ruta", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="viajes", to="rutas.ruta")),
            ],
            options={"ordering": ["-fecha", "horario__salida", "id"]},
        ),
        migrations.CreateModel(
            name="PosicionDeViaje",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("id_cliente", models.CharField(max_length=64)),
                ("latitud", models.FloatField()),
                ("longitud", models.FloatField()),
                ("tomada_en", models.DateTimeField()),
                ("recibida_en", models.DateTimeField(auto_now_add=True)),
                ("viaje", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="posiciones", to="viajes.viaje")),
            ],
            options={"ordering": ["tomada_en", "id"]},
        ),
        migrations.AddConstraint(
            model_name="viaje",
            constraint=models.UniqueConstraint(condition=models.Q(("estado", "en_curso")), fields=("chofer",), name="un_viaje_en_curso_por_chofer"),
        ),
        migrations.AddConstraint(
            model_name="posiciondeviaje",
            constraint=models.UniqueConstraint(fields=("viaje", "id_cliente"), name="posicion_de_viaje_unica"),
        ),
    ]
