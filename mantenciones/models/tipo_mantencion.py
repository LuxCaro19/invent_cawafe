from django.db import models

class Tipo_mantencion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    frecuencia_dias = models.PositiveIntegerField(default=30)

    def __str__(self):
        return self.nombre

class Tarea_tipo_mantencion(models.Model):
    tipo = models.ForeignKey(Tipo_mantencion, on_delete=models.CASCADE, related_name='tareas')
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.tipo.nombre} - {self.descripcion}"
