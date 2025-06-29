import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invent_cawafe.settings')
django.setup()

from inventario.models import *
from mantenciones.models import *
from usuarios.models import Usuario
from django.contrib.auth.hashers import make_password
from usuarios.models import *
from inventario.models import *
# Crear marcas, tipos y modelos
marca = Modelo_marca.objects.get_or_create(marca='Generica')[0]
tipos = {tipo: Modelo_tipo.objects.get_or_create(tipo=tipo)[0] for tipo in ['Notebook', 'Desktop', 'Monitor']}

modelos = {}
for tipo, obj in tipos.items():
    modelos[tipo] = Modelo_equipo.objects.get_or_create(nombre=f'{tipo} 2025', tipo=obj, marca=marca, precio=500000)[0]

# Sistema Operativo, Procesador, Estado
so = Sistema_operativo.objects.get_or_create(nombre='Windows 11', marca=marca)[0]
proc = Procesador.objects.get_or_create(nombre='Intel i5', marca=marca)[0]
estado = Estado_equipo.objects.get_or_create(nombre='Operativo')[0]

# Crear ubicaciones
ubic = Ubicacion.objects.get_or_create(nombre='Oficina Central')[0]

# Crear usuarios
usuarios = []
for i in range(1, 6):
    user = Usuario.objects.get_or_create(
        correo=f'user{i}@test.cl',
        defaults={
            'password': make_password('test1234'),
            'nombre_completo': f'Usuario {i}',
            'rut': f'1111111{i}-k',
            'ubicacion': ubic,
            'cargo': 'Técnico',
            'is_active': True,
            'is_staff': False
        }
    )[0]
    usuarios.append(user)

# Crear 200 equipos
contador = {'Notebook': 1, 'Desktop': 1, 'Monitor': 1}
equipos = []
for tipo in ['Notebook', 'Desktop', 'Monitor']:
    for _ in range(0, 200 // 3):
        etiqueta = f"{tipo[:3].upper()}K{contador[tipo]:05d}"
        equipo = Equipo.objects.create(
            etiqueta=etiqueta,
            modelo=modelos[tipo],
            memoria_ram=random.choice([4, 8, 16]),
            almacenamiento=random.choice([128, 256, 512]),
            numero_serie=f"SERIE{contador[tipo]:05d}",
            fecha_de_compra=datetime.now().date() - timedelta(days=random.randint(0, 1000)),
            imei=f"IMEI{contador[tipo]:05d}" if tipo == 'Notebook' else None,
            mac=f"00:1A:C2:{random.randint(10, 99)}:{random.randint(10, 99)}:{contador[tipo]:02d}",
            en_bodega=random.choice([True, False]),
            sistema_operativo=so,
            procesador=proc,
            estado=estado,
            usuario_asignado=random.choice(usuarios)
        )
        contador[tipo] += 1
        equipos.append(equipo)

# Crear tipo de mantención
tipo_mant = Tipo_mantencion.objects.get_or_create(
    nombre="Mantención Anual", frecuencia_dias=365,
    modelo_tipo=modelos['Notebook'].tipo, sistema_operativo=so
)[0]

# Crear tareas por tipo
tareas = []
for desc in ['Limpiar ventilador', 'Actualizar drivers', 'Verificar RAM']:
    tarea = Tarea_tipo_mantencion.objects.get_or_create(tipo=tipo_mant, descripcion=desc)[0]
    tareas.append(tarea)

# Crear mantenciones y registros
for equipo in equipos[:100]:  # Solo para los primeros 100
    mant = Mantencion.objects.get_or_create(equipo=equipo, tipo=tipo_mant)[0]
    reg = Registro_mantencion.objects.create(
        mantencion=mant,
        fecha=datetime.now().date() - timedelta(days=random.randint(1, 100)),
        tipo='Preventiva',
        responsable=random.choice(usuarios),
        observaciones='Equipo mantenido correctamente.',
        ubicacion=ubic.nombre
    )
    for tarea in tareas:
        Tarea_realizada.objects.create(registro=reg, tarea=tarea, descripcion=tarea.descripcion, realizada=True)
    Equipo_historial.objects.create(
        equipo=equipo,
        usuario_asignado=equipo.usuario_asignado,
        estado="Mantenido",
        fecha=datetime.now(),
        registrado_por=random.choice(usuarios)
    )

print("Población masiva completada.")
