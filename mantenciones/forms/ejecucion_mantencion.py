from django import forms
from mantenciones.models import Registro_mantencion

class Ejecutar_Mantencion(forms.ModelForm):
    class Meta:
        model = Registro_mantencion
        fields = ['ubicacion', 'observaciones']  # Excluimos 'responsable'
        widgets = {
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
