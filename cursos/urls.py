from django.urls import path
from . import views_public as v
from . import views

app_name = "cursos"

urlpatterns = [
    path("", views.cursos_catalogo, name="catalogo"),
    path("<int:pk>/", v.cursos_detalle, name="detalle"),
     path("<int:pk>/inscribirme/", views.inscribirme, name="inscribirme"),
]