from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render

from .models import Inscripcion


@login_required
def mis_cursos_lista(request):
    usuario = request.user

    # Solo estudiante o admin (MVP)
    if not (getattr(usuario, "es_estudiante", False) or getattr(usuario, "es_administrador", False)):
        raise PermissionDenied

    inscripciones = (
        Inscripcion.objects
        .filter(estudiante=usuario)
        .select_related("curso", "curso__docente")
    )

    return render(request, "lms/mis_cursos/lista.html", {"inscripciones": inscripciones})


@login_required
def mis_cursos_detalle(request, pk: int):
    usuario = request.user

    if not (getattr(usuario, "es_estudiante", False) or getattr(usuario, "es_administrador", False)):
        raise PermissionDenied

    inscripcion = get_object_or_404(
        Inscripcion.objects.select_related("curso", "curso__docente"),
        estudiante=usuario,
        curso_id=pk,
    )

    return render(request, "lms/mis_cursos/detalle.html", {"curso": inscripcion.curso})