from django.db import models
from .modelo_equipo import Modelo_equipo
from .procesador import Procesador
from .estado_equipo import Estado_equipo
from .sistema_operativo import Sistema_operativo

# Create your models here.

class Equipo(models.Model):
    etiqueta = models.CharField()
    memoria_ram = models.IntegerField(null=True)
    almacenamiento = models.IntegerField(null=True)
    modelo = models.ForeignKey(Modelo_equipo, on_delete=models.SET_NULL, null=True )
    sistema_operativo = models.ForeignKey(Sistema_operativo, on_delete=models.SET_NULL, null=True )
    procesador = models.ForeignKey(Procesador, on_delete=models.SET_NULL, null=True )
    estado = models.ForeignKey(Estado_equipo, on_delete=models.SET_NULL, null=True )

    def __str__(self):
        return self.etiqueta

