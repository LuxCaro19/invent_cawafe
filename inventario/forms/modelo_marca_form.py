from django import forms
from inventario.models.modelo_marca import Modelo_marca

class Modelo_marcaForm(forms.ModelForm):
    class Meta:
        model = Modelo_marca
        fields = ['marca']
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100%;'}),
        }
