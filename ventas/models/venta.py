from django.db import models
from django.utils import timezone


class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_venta = models.DateField(null=True)  
    id_equipo = models.ForeignKey('inventario.Equipo', on_delete=models.SET_NULL, null=True)
    #id_usuario = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    nombre_receptor = models.CharField(max_length=100, null=True)
    flag_aprobado_remuneraciones = models.BooleanField(default=None)
    flag_entregado = models.BooleanField(default=False)





    
