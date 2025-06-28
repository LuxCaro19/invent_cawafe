from django.db import models
from .mantencion import Mantencion
from usuarios.models import Usuario
from .tipo_mantencion import Tarea_tipo_mantencion

class Registro_mantencion(models.Model):
    mantencion = models.ForeignKey(Mantencion, on_delete=models.CASCADE, related_name='registros')
    fecha = models.DateField(auto_now_add=True)
    tipo = models.CharField(max_length=100, default="Desconocido") 
    responsable = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='responsable_mantencion')
    observaciones = models.TextField(blank=True, null=True)
    ubicacion = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.mantencion.equipo} - {self.observaciones}"

class Tarea_realizada(models.Model):
    registro = models.ForeignKey(Registro_mantencion, on_delete=models.CASCADE, related_name='tareas_realizadas')
    tarea = models.ForeignKey(Tarea_tipo_mantencion, on_delete=models.SET_NULL, null=True, blank=True)
    descripcion = models.CharField(max_length=255)
    realizada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.descripcion} - {'✔' if self.realizada else '✗'}"
    


