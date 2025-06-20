from django.db import models

# Create your models here.

class Modelo_tipo(models.Model):
    tipo = models.CharField()

    def __str__(self):  
        return self.tipo
    
    def eliminar_tipo(self):
        self.delete()

    def modificar_tipo(self, form):
        # Actualiza otros campos del formulario
        for campo in form.cleaned_data:
            setattr(self, campo, form.cleaned_data[campo])

        self.save()