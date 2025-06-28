from mantenciones.models import Tipo_mantencion, Mantencion, Registro_mantencion
from usuarios.models import Usuario

def crear_mantencion_inicial_para_equipo(equipo, usuario=None):
    tipo, _ = Tipo_mantencion.objects.get_or_create(
        nombre='Creación',
        defaults={'frecuencia_dias': 0}
    )

    mantencion = Mantencion.objects.create(equipo=equipo, tipo=tipo)

    if usuario is None:
        usuario, _ = Usuario.objects.get_or_create(
            correo='sistema@local',
            defaults={
                'nombre_completo': 'Sistema Mantenciones',
                'rut': '0-0',
                'is_active': False,
                'is_staff': False
            }
        )

    Registro_mantencion.objects.create(
        mantencion=mantencion,
        responsable=usuario,
        observaciones='Mantención inicial al crear equipo',
        ubicacion='Desconocida',
        tipo='Inicial'
    )