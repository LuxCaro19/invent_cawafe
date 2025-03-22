from django import forms
from inventario.models.equipo import Equipo

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['etiqueta', 'memoria_ram', 'almacenamiento']

    