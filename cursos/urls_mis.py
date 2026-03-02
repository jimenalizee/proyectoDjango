from django.urls import path
from . import views_mis as views

app_name = "mis_cursos"

urlpatterns = [
    path("", views.mis_cursos_lista, name="lista"),
    path("<int:pk>/", views.mis_cursos_detalle, name="detalle"),
]