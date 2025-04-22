from django import forms
from inventario.models.modelo_tipo import Modelo_tipo

class Tipo_equipoForm(forms.ModelForm):
    class Meta:
        model = Modelo_tipo
        fields = ['tipo']
        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100%;'}),
        }
