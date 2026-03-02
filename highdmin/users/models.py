from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for highdmin_django.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    class Rol(models.TextChoices):
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador"
        DOCENTE = "DOCENTE", "Docente"
        ESTUDIANTE = "ESTUDIANTE", "Estudiante"

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    # Nuevo campo para mini-LMS
    rol = models.CharField(
        _("Rol"),
        max_length=20,
        choices=Rol.choices,
        default=Rol.ESTUDIANTE,
        help_text="Rol funcional para el mini-LMS",
    )

    def get_absolute_url(self) -> str:
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def es_administrador(self) -> bool:
        return self.is_superuser or self.rol == self.Rol.ADMINISTRADOR

    @property
    def es_docente(self) -> bool:
        return self.rol == self.Rol.DOCENTE

    @property
    def es_estudiante(self) -> bool:
        return self.rol == self.Rol.ESTUDIANTE