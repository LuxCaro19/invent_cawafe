from django.db import models
from .modelo_marca import Modelo_marca

class Procesador(models.Model):
    nombre = models.CharField()
    marca = models.ForeignKey(Modelo_marca, on_delete=models.SET_NULL, null=True )

    def __str__(self):  
        return self.nombre