from django.utils.timezone import now
from mantenciones.models import Mantencion, Registro_mantencion, Tipo_mantencion
from inventario.models import Equipo

def sincronizar_mantenciones():
    try:
        tipo_creacion = Tipo_mantencion.objects.get(nombre__iexact='Creación')
    except Tipo_mantencion.DoesNotExist:
        print("Tipo de mantención 'Creación' no existe.")
        return

    total_creadas = 0
    total_registros_agregados = 0
    Tipo_mantencion.objects.create(nombre='Creación', frecuencia_dias=30)
    
    # Crear mantenciones para equipos que no tienen
    for equipo in Equipo.objects.all():
        if not Mantencion.objects.filter(equipo=equipo).exists():
            mantencion = Mantencion.objects.create(equipo=equipo, tipo=tipo_creacion)
            Registro_mantencion.objects.create(
                mantencion=mantencion,
                fecha=now(),
                responsable='Sincronización automática',
                ubicacion=getattr(equipo, 'ubicacion', 'Desconocida'),
                observaciones='Registro inicial por sincronización'
            )
            total_creadas += 1

    # Asegurar que todas las mantenciones tengan al menos un registro
    for mantencion in Mantencion.objects.all():
        if not mantencion.registros.exists():
            Registro_mantencion.objects.create(
                mantencion=mantencion,
                fecha=now(),
                responsable='Sincronización automática',
                ubicacion=getattr(mantencion.equipo, 'ubicacion', 'Desconocida'),
                observaciones='Registro agregado por sincronización'
            )
            total_registros_agregados += 1

    print(f"Sincronización completa. Mantenciones nuevas: {total_creadas}, registros agregados: {total_registros_agregados}")
