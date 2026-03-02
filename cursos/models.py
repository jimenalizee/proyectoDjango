from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models


class Curso(models.Model):
    docente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cursos_como_docente",
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    activo = models.BooleanField(default=True)
    carga_horaria = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["-fecha_inicio", "-id"]

    def __str__(self) -> str:
        return self.titulo
    
class Inscripcion(models.Model):
    curso = models.ForeignKey("Curso", on_delete=models.CASCADE, related_name="inscripciones")
    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="inscripciones",
    )
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["curso", "estudiante"],
                name="uniq_inscripcion_curso_estudiante",
            )
        ]
        ordering = ["-fecha_inscripcion", "-id"]

    def __str__(self):
        return f"{self.estudiante} -> {self.curso}"