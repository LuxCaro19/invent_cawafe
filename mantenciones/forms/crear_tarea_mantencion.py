
from mantenciones.models import Tarea_tipo_mantencion
from django import forms

class TareaTipoMantencionForm(forms.ModelForm):
    class Meta:
        model = Tarea_tipo_mantencion
        fields = ['descripcion']