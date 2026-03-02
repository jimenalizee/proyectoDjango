from django.contrib import admin
from .models import Curso
from .models import Inscripcion

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "docente", "fecha_inicio", "activo")
    list_filter = ("activo", "fecha_inicio")
    search_fields = ("titulo", "docente__username", "docente__email")

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ("id", "curso", "estudiante", "fecha_inscripcion")
    search_fields = ("curso__titulo", "estudiante__username", "estudiante__email")
    list_filter = ("fecha_inscripcion",)