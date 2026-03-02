from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import CursoForm
from .models import Curso


class DocenteOAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        u = self.request.user
        return u.is_authenticated and (getattr(u, "es_administrador", False) or getattr(u, "es_docente", False))


class CursoPanelListView(DocenteOAdminMixin, ListView):
    model = Curso
    template_name = "lms/panel_cursos/lista.html"
    context_object_name = "cursos"

    def get_queryset(self):
        u = self.request.user
        qs = Curso.objects.select_related("docente")
        if getattr(u, "es_administrador", False):
            return qs
        return qs.filter(docente=u)


class CursoCreateView(DocenteOAdminMixin, CreateView):
    model = Curso
    form_class = CursoForm
    template_name = "lms/panel_cursos/form.html"
    success_url = reverse_lazy("cursos_panel:lista")

    def form_valid(self, form):
        form.instance.docente = self.request.user
        return super().form_valid(form)


class CursoUpdateView(DocenteOAdminMixin, UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = "lms/panel_cursos/form.html"
    success_url = reverse_lazy("cursos_panel:lista")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        u = self.request.user
        if getattr(u, "es_administrador", False) or obj.docente_id == u.id:
            return obj
        raise PermissionDenied


class CursoDeleteView(DocenteOAdminMixin, DeleteView):
    model = Curso
    template_name = "lms/panel_cursos/confirm_delete.html"
    success_url = reverse_lazy("cursos_panel:lista")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        u = self.request.user
        if getattr(u, "es_administrador", False) or obj.docente_id == u.id:
            return obj
        raise PermissionDenied