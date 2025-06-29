from django.db import models
from inventario.models import Modelo_tipo,Sistema_operativo

class Tipo_mantencion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    frecuencia_dias = models.PositiveIntegerField(default=30)

    modelo_tipo = models.ForeignKey(
        Modelo_tipo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tipos_mantencion'
    )

    sistema_operativo = models.ForeignKey(
        Sistema_operativo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tipos_mantencion_so'
    )

    def __str__(self):
        return self.nombre


class Tarea_tipo_mantencion(models.Model):
    tipo = models.ForeignKey(Tipo_mantencion, on_delete=models.CASCADE, related_name='tareas')
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.tipo.nombre} - {self.descripcion}"
