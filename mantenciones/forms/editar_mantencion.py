from django import forms
from mantenciones.models import Mantencion

class Editar_mantencion(forms.ModelForm):
    class Meta:
        model = Mantencion
        fields = ['tipo']
