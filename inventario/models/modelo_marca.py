from django.db import models

# Create your models here. 

class Modelo_marca(models.Model):
    marca = models.CharField()

    def __str__(self):  
        return self.marca
    
    def eliminar_marca(self):
        self.delete()

    def modificar_marca(self, form):
        # Actualiza otros campos del formulario
        for campo in form.cleaned_data:
            setattr(self, campo, form.cleaned_data[campo])

        self.save()     

    