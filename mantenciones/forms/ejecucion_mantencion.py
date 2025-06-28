from django import forms
from mantenciones.models import Registro_mantencion

class Ejecutar_Mantencion(forms.ModelForm):
    class Meta:
        model = Registro_mantencion
        fields = ['responsable', 'ubicacion', 'observaciones']
        widgets = {
            'responsable': forms.TextInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
