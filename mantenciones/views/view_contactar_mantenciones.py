from django.shortcuts import render
from mantenciones.models import Mantencion
from usuarios.models import Usuario
from parametro.models import Ubicacion
from inventario.models import Equipo, Estado_equipo

# Agregar al inicio:
from django.db.models import Q
from inventario.models import Equipo, Estado_equipo

def contactar_mantenciones(request):
    ids = request.GET.getlist('ids')
    mantenciones = Mantencion.objects.filter(id__in=ids).select_related(
        'equipo__modelo__tipo',
        'equipo__usuario_asignado__ubicacion'
    )

    correos = set()
    conteo_usuarios = {}
    ubicacion_por_usuario = {}
    equipos_por_usuario = {}

    usuarios_ids = set()

    # Extraer ubicación seleccionada (viene como string desde el <select>)
    ubicacion_seleccionada_id = request.GET.get("ubicacion") or None

    # Fase 1: Obtener usuarios desde las mantenciones
    for m in mantenciones:
        equipo = m.equipo
        usuario = getattr(equipo, 'usuario_asignado', None)

        if usuario:
            usuarios_ids.add(usuario.id)
            conteo_usuarios[usuario.id] = conteo_usuarios.get(usuario.id, 0) + 1
            ubicacion_por_usuario[usuario.id] = usuario.ubicacion

            if usuario.correo:
                correos.add(usuario.correo)

    # Fase 2: Buscar todos los equipos operativos de estos usuarios
    estado_operativo = Estado_equipo.objects.filter(nombre__iexact="operativo").first()
    equipos_operativos = []

    if estado_operativo and usuarios_ids:
        filtros = Q(usuario_asignado__id__in=usuarios_ids, estado=estado_operativo)

        if ubicacion_seleccionada_id:
            filtros &= Q(ubicacion__id=ubicacion_seleccionada_id)

        equipos_operativos = Equipo.objects.filter(filtros).select_related(
            'modelo__tipo', 'usuario_asignado', 'usuario_asignado__ubicacion'
        )

    # Agrupar por usuario
    for equipo in equipos_operativos:
        usuario = equipo.usuario_asignado
        key = f"{usuario.nombre_completo} ({usuario.cargo or 'Sin cargo'})" if usuario else "Sin asignar (Sin cargo)"

        tipo_equipo = getattr(getattr(equipo, 'modelo', None), 'tipo', None)
        nombre_tipo = str(tipo_equipo) if tipo_equipo else "Equipo"

        equipos_por_usuario.setdefault(key, []).append(nombre_tipo)

    # Resumen
    equipos_resumen = {}
    for usuario, lista_equipos in equipos_por_usuario.items():
        resumen = {}
        for tipo in lista_equipos:
            resumen[tipo] = resumen.get(tipo, 0) + 1
        equipos_resumen[usuario] = ', '.join(f"{v} {k}" for k, v in resumen.items())

    # Selección automática solo si no se recibe una ubicación por GET
    if not ubicacion_seleccionada_id:
        usuario_destacado_id = max(conteo_usuarios, key=conteo_usuarios.get) if conteo_usuarios else None
        ubicacion_seleccionada = ubicacion_por_usuario.get(usuario_destacado_id) if usuario_destacado_id else None
        ubicacion_seleccionada_id = ubicacion_seleccionada.id if ubicacion_seleccionada else None
    else:
        usuario_destacado_id = None

    return render(request, 'contactar_mantenciones.html', {
        'mantenciones': mantenciones,
        'correos': sorted(correos),
        'usuarios': Usuario.objects.all(),
        'usuario_destacado_id': usuario_destacado_id,
        'ubicaciones': Ubicacion.objects.all(),
        'ubicacion_seleccionada_id': int(ubicacion_seleccionada_id) if ubicacion_seleccionada_id else None,
        'equipos_por_usuario': equipos_resumen,
    })
