from django import forms
from inventario.models.modelo_equipo import Modelo_equipo
from inventario.models.modelo_marca import Modelo_marca
from inventario.models.modelo_tipo import Modelo_tipo

class Modelo_equipoForm(forms.ModelForm):

    tipo = forms.ModelChoiceField(
        queryset=Modelo_tipo.objects.all(), 
        empty_label="Seleccione un tipo", 
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'tipo'})
    )

    marca = forms.ModelChoiceField(
        queryset=Modelo_marca.objects.all(), 
        empty_label="Seleccione una marca", 
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'marca'})
    )

    class Meta:
        model = Modelo_equipo
        fields = ['nombre', 'tipo', 'marca', 'precio'] 
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        }
