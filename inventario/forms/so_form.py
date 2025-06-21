from django import forms
from inventario.models.sistema_operativo import Sistema_operativo

class SoForm(forms.ModelForm):
    class Meta:
        model = Sistema_operativo
        fields = ['nombre', 'marca']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100%;'}),
            'marca': forms.Select(attrs={'class': 'form-control select2' , 'style': 'width: 100%;'})
        }
