from django.db import models
from .modelo_marca import Modelo_marca

class Sistema_operativo(models.Model):
    nombre = models.CharField()
    marca = models.ForeignKey(Modelo_marca, on_delete=models.SET_NULL, null=True )