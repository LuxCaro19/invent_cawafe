from django.db import models
from inventario.models import Equipo
from usuarios.models import Usuario
from django.contrib.auth.models import User
from django.conf import settings  # ← Agrega esta importación


from django.db import models
from inventario.models import Equipo
from usuarios.models import Usuario
from django.conf import settings

class HistorialEquipo(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    usuario_asignado = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='historial_asignado'
    )
    estado = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='historial_registrado'
    )

    def __str__(self):
        return f"{self.equipo.nombre} - {self.estado} ({self.fecha.strftime('%Y-%m-%d %H:%M')})"
