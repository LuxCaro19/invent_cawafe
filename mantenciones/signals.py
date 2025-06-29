from django.db.models.signals import post_save
from django.dispatch import receiver

from inventario.models import Equipo
from mantenciones.models import Mantencion, Registro_mantencion, Tipo_mantencion
from usuarios.models import Usuario  # Ajusta si está en otro módulo

@receiver(post_save, sender=Equipo)
def crear_mantencion_al_crear_equipo(sender, instance, created, **kwargs):
    if not created:
        return

    # Buscar o crear el tipo "Creación"
    tipo, _ = Tipo_mantencion.objects.get_or_create(
        nombre='Creación',
        defaults={'frecuencia_dias': 0}
    )

    # Crear o recuperar el usuario "Sistema Mantenciones"
    sistema, _ = Usuario.objects.get_or_create(
        correo='sistema@local',
        defaults={
            'nombre_completo': 'Sistema Mantenciones',
            'rut': '0-0',
            'is_active': False,
            'is_staff': False
        }
    )

    # Crear la mantención para el equipo
    mantencion = Mantencion.objects.create(equipo=instance, tipo=tipo)

    # Crear el primer registro
    Registro_mantencion.objects.create(
        mantencion=mantencion,
        responsable=sistema,
        observaciones='Equipo agregado al sistema de mantencion.',
        ubicacion='Desconocida',
        tipo='Inicial'
    )
