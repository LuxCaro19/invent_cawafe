from django import forms
from mantenciones.models import Tipo_mantencion
from inventario.models import Modelo_tipo, Sistema_operativo

class TipoMantencionForm(forms.ModelForm):
    modelo_tipo = forms.ModelChoiceField(
        queryset=Modelo_tipo.objects.all(),
        required=False,
        empty_label="Tipo de equipo no encontrado",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    sistema_operativo = forms.ModelChoiceField(
        queryset=Sistema_operativo.objects.all(),
        required=False,
        empty_label="Sistema operativo no encontrado",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Tipo_mantencion
        fields = ['nombre', 'frecuencia_dias', 'modelo_tipo', 'sistema_operativo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'frecuencia_dias': forms.NumberInput(attrs={'class': 'form-control'}),
        }
