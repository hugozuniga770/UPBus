"""La cuenta de UPBus (HU-01, HU-02, HU-03)."""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, correo, password=None, **extra):
        if not correo:
            raise ValueError("El correo es obligatorio")
        usuario = self.model(correo=self.normalize_email(correo).lower(), **extra)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, correo, password=None, **extra):
        extra.setdefault("rol", Usuario.Rol.ADMINISTRADOR)
        extra.setdefault("nombre", "Administrador")
        extra["is_staff"] = True
        extra["is_superuser"] = True
        return self.create_user(correo, password, **extra)


class Usuario(AbstractBaseUser, PermissionsMixin):
    class Rol(models.TextChoices):
        ESTUDIANTE = "estudiante", "Estudiante"
        CHOFER = "chofer", "Chofer"
        ADMINISTRADOR = "administrador", "Administrador"

    correo = models.EmailField(unique=True)
    # Los choferes no están en el padrón: su código queda vacío (BUS-RF-04).
    codigo = models.CharField(max_length=20, unique=True, null=True, blank=True)
    nombre = models.CharField(max_length=150)
    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.ESTUDIANTE)
    is_active = models.BooleanField("activa", default=True)
    is_staff = models.BooleanField("entra al panel de Django", default=False)
    creado_en = models.DateTimeField(auto_now_add=True)

    objects = UsuarioManager()

    USERNAME_FIELD = "correo"
    EMAIL_FIELD = "correo"
    REQUIRED_FIELDS = ["nombre"]

    class Meta:
        verbose_name = "cuenta"
        verbose_name_plural = "cuentas"
        ordering = ["rol", "nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.get_rol_display()})"

    @property
    def es_administrador(self):
        return self.rol == self.Rol.ADMINISTRADOR

    @property
    def es_chofer(self):
        return self.rol == self.Rol.CHOFER

    @property
    def puede_actuar_como_estudiante(self):
        """Un administrador también es estudiante (sesión 6, sección 2)."""
        return self.rol in (self.Rol.ESTUDIANTE, self.Rol.ADMINISTRADOR)
