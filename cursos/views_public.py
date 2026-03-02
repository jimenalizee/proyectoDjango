from django.shortcuts import get_object_or_404, render
from .models import Curso
from django.contrib.auth.decorators import login_required


def cursos_detalle(request, pk: int):
    curso = get_object_or_404(
        Curso.objects.select_related("docente"),
        pk=pk,
        activo=True,
    )
    return render(request, "lms/cursos/detalle.html", {"curso": curso})