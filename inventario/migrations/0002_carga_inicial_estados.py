from django.db import migrations

def crear_datos_iniciales(apps, schema_editor):
    EstadoEquipo = apps.get_model('inventario', 'Estado_equipo')
    Ubicacion = apps.get_model('inventario', 'Ubicacion')  # Asegúrate de que existe el modelo

    # Crear estados iniciales
    estados = ['Operativo', 'Robado', 'Obsoleto', 'Asignado','En bodega','Por Vender','Pendiente RRHH','Pendiente Entrega','Vendido']
    for estado in estados:
        EstadoEquipo.objects.get_or_create(nombre=estado)

    # Crear ubicación "En Bodega"
    Ubicacion.objects.get_or_create(nombre="En Bodega")


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_datos_iniciales),
    ]
