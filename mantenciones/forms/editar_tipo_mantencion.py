from django import forms
from mantenciones.models import Tipo_mantencion

class TipoMantencionEditarForm(forms.ModelForm):
    class Meta:
        model = Tipo_mantencion
        fields = ['nombre', 'frecuencia_dias', 'modelo_tipo', 'sistema_operativo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['frecuencia_dias'].widget.attrs.update({'class': 'form-control'})
        self.fields['modelo_tipo'].widget.attrs.update({'class': 'form-select'})
        self.fields['sistema_operativo'].widget.attrs.update({'class': 'form-select'})
