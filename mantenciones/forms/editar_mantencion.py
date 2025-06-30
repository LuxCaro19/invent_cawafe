from django import forms
from mantenciones.models import Mantencion, Tipo_mantencion

class Editar_mantencion(forms.ModelForm):
    class Meta:
        model = Mantencion
        fields = ['tipo']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        tipos_queryset = kwargs.pop('tipos_queryset', None)
        super().__init__(*args, **kwargs)

        if tipos_queryset is not None:
            self.fields['tipo'].queryset = tipos_queryset
