from django import forms
from .models import Curso


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ["titulo", "descripcion", "fecha_inicio", "activo", "carga_horaria"]
        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Aplicar clases bootstrap a campos
        for name, field in self.fields.items():
            if name == "activo":
                field.widget.attrs.update({"class": "form-check-input"})
            elif name != "fecha_inicio":
                field.widget.attrs.update({"class": "form-control"})