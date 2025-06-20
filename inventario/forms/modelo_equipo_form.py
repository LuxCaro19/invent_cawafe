from django import forms
from inventario.models.modelo_equipo import Modelo_equipo
from inventario.models.modelo_marca import Modelo_marca
from inventario.models.modelo_tipo import Modelo_tipo

class Modelo_equipoForm(forms.ModelForm):
    class Meta:
        model = Modelo_equipo
        fields = ['nombre', 'marca', 'tipo', 'precio']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100%;'}),
            'marca': forms.Select(attrs={'class': 'form-control select2' , 'style': 'width: 100%;'}),
            'tipo': forms.Select(attrs={'class': 'form-control', 'style': 'width: 100%;'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100%;'}),
        }
