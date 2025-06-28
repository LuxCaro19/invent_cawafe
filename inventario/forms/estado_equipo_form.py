from django import forms
from inventario.models.estado_equipo import Estado_equipo

class Estado_equipoForm(forms.ModelForm):
    class Meta:
        model = Estado_equipo
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100%;'}),
        }
