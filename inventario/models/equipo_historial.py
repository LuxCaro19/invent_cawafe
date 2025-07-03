from django.db import models
from django.utils import timezone
from .equipo import Equipo
from .estado_equipo import Estado_equipo

class Equipo_historial(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)
    estado_anterior = models.ForeignKey(Estado_equipo, on_delete=models.SET_NULL, null=True, blank=True, related_name='estado_anterior')
    nuevo_estado = models.ForeignKey(Estado_equipo, on_delete=models.SET_NULL, null=True, blank=True, related_name='nuevo_estado')
    observaciones = models.TextField(blank=True, null=True)  # ← Asegúrate de tener esta línea

    def __str__(self):
        return f"{self.equipo} - {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}"
