from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from .models import Curso, Inscripcion
# Create your views here.
def landing_home(request):
    cursos = (
        Curso.objects
        .filter(activo=True)
        .select_related("docente")
        .order_by("-fecha_inicio", "-id")[:12]
    )
    return render(request, "pages/index.html", {"cursos": cursos})

@login_required
def cursos_catalogo(request):
    cursos = Curso.objects.filter(activo=True).select_related("docente")
    return render(request, "lms/cursos/catalogo.html", {"cursos": cursos})

@login_required
def inscribirme(request, pk: int):
    if request.method != "POST":
        return redirect("cursos:detalle", pk=pk)

    usuario = request.user

    # Solo estudiantes (MVP didáctico)
    if not getattr(usuario, "es_estudiante", False) and not getattr(usuario, "es_administrador", False):
        messages.error(request, "Solo estudiantes pueden inscribirse (MVP).")
        return redirect("cursos:detalle", pk=pk)

    curso = get_object_or_404(Curso, pk=pk, activo=True)

    insc, created = Inscripcion.objects.get_or_create(curso=curso, estudiante=usuario)
    if created:
        messages.success(request, "Inscripción realizada correctamente.")
    else:
        messages.info(request, "Ya estabas inscrito en este curso.")

    return redirect("mis_cursos:lista")