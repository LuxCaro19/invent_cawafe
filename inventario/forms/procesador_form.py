from django import forms
from inventario.models.procesador import Procesador

class ProcesadorForm(forms.ModelForm):
    class Meta:
        model = Procesador
        fields = ['nombre', 'marca']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100%;'}),
            'marca': forms.Select(attrs={'class': 'form-control select2' , 'style': 'width: 100%;'})
        }
