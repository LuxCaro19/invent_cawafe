from django import forms
from inventario.models.equipo import Equipo

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['etiqueta', 'memoria_ram', 'almacenamiento', 'modelo', 'sistema_operativo', 'procesador', 'numero_serie', 'estado']
        widgets = {
            'etiqueta': forms.TextInput(attrs={'class': 'form-control'}),
            'memoria_ram': forms.NumberInput(attrs={'class': 'form-control'}),
            'almacenamiento': forms.NumberInput(attrs={'class': 'form-control'}),
            'modelo': forms.Select(attrs={'class': 'form-control select2' , 'style': 'width: 100%;'}),
            'sistema_operativo': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'procesador': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

        
    