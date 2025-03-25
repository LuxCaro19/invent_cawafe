from django.db import models
from .equipo import Equipo

class Equipo_historial(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField()
    estado = models.ForeignKey('inventario.Estado_equipo', on_delete=models.SET_NULL, null=True)