from django.db import models
from inventario.models import Equipo
from .tipo_mantencion import Tipo_mantencion

class Mantencion(models.Model):
    equipo = models.OneToOneField(Equipo, on_delete=models.CASCADE, unique=True)
    tipo = models.ForeignKey(Tipo_mantencion, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.equipo} - {self.tipo} ({self.fecha_proxima})"

    @property
    def fecha_proxima(self):
        from datetime import timedelta
        ultima = self.ultima_fecha()
        if self.tipo and ultima:
            return ultima + timedelta(days=self.tipo.frecuencia_dias)
        return None

    def ultima_fecha(self):
        ultimo = self.registros.order_by('-fecha').first()
        return ultimo.fecha if ultimo else None
