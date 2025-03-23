from django import forms
from models.modelo_equipo import Modelo_equipo

class Modelo_equipoForm(forms.ModelForm):
    class Meta:
        model = Modelo_equipo
        fields = ['nombre', 'tipo', 'marca', 'precio'] 
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.Select(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        }