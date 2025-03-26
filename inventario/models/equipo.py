from django.db import models
from django.utils import timezone
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

    def cambiar_estado(self, nuevo_estado):
        from .equipo_historial import Equipo_historial

        if self.pk:
            estado_actual = Equipo.objects.get(pk=self.pk).estado
        else:
            estado_actual = None

        if estado_actual != nuevo_estado:
            Equipo_historial.objects.create(
                equipo=self,
                fecha=timezone.now(),
                estado_anterior=estado_actual,
                nuevo_estado=nuevo_estado
            )
        self.estado = nuevo_estado

    def modificar_equipo(self, form):
        nuevo_estado = form.cleaned_data['estado']
        self.cambiar_estado(nuevo_estado)

        # Actualiza otros campos del formulario
        for campo in form.cleaned_data:
            if campo != 'estado':
                setattr(self, campo, form.cleaned_data[campo])

        self.save()

    def eliminar_equipo(self):
        self.delete()