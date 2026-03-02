from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from highdmin.users.models import User

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def panel_demo(request):
    return render(request, "lms/panel_demo.html")

@login_required
def perfil_view(request):
    return render(request, "lms/perfil.html", {"usuario": request.user})


@login_required
def panel_view(request):
    usuario = request.user

    if usuario.is_superuser:
        rol_mostrado = "ADMINISTRADOR"
    else:
        rol_mostrado = getattr(usuario, "rol", "SIN_ROL")

    mensaje = "Bienvenido al panel del mini-LMS."
    if rol_mostrado == "ADMINISTRADOR":
        mensaje = "Acceso total al sistema (MVP)."
    elif rol_mostrado == "DOCENTE":
        mensaje = "Panel de docente: gestión de cursos y lecciones (siguiente guía)."
    elif rol_mostrado == "ESTUDIANTE":
        mensaje = "Panel de estudiante: cursos inscritos (siguiente guía)."

    return render(
        request,
        "lms/panel.html",
        {
            "usuario": usuario,
            "rol_mostrado": rol_mostrado,
            "mensaje": mensaje,
        },
    )


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Nombre de usuario actualizado")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None=None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()

@login_required
def perfil_view(request):
    return render(request, "lms/perfil.html", {"usuario": request.user})


@login_required
def panel_view(request):
    usuario = request.user

    if usuario.is_superuser:
        rol_mostrado = "ADMINISTRADOR"
    else:
        rol_mostrado = getattr(usuario, "rol", "SIN_ROL")

    mensaje = "Bienvenido al panel del mini-LMS."
    if rol_mostrado == "ADMINISTRADOR":
        mensaje = "Acceso total al sistema (MVP)."
    elif rol_mostrado == "DOCENTE":
        mensaje = "Panel de docente: gestión de cursos y lecciones (siguiente guía)."
    elif rol_mostrado == "ESTUDIANTE":
        mensaje = "Panel de estudiante: cursos inscritos (siguiente guía)."

    return render(
        request,
        "lms/panel.html",
        {
            "usuario": usuario,
            "rol_mostrado": rol_mostrado,
            "mensaje": mensaje,
        },
    )