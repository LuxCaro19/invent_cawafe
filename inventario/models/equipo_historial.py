from django.db import models
from .equipo import Equipo

class Equipo_historial(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE , null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    estado_anterior = models.ForeignKey('inventario.Estado_equipo', on_delete=models.SET_NULL, null=True, related_name='estado_anterior')
    nuevo_estado = models.ForeignKey('inventario.Estado_equipo', on_delete=models.SET_NULL, null=True, related_name='estado_nuevo')
