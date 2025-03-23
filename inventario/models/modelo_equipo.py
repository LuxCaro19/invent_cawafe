from django.db import models
from .modelo_marca import Modelo_marca
from .modelo_tipo import Modelo_tipo

class Modelo_equipo(models.Model):
    nombre = models.CharField()
    tipo = models.ForeignKey(Modelo_tipo, on_delete=models.SET_NULL, null=True )
    marca = models.ForeignKey(Modelo_marca, on_delete=models.SET_NULL, null=True )
    precio = models.IntegerField()

    def __str__(self):  
        return self.nombre