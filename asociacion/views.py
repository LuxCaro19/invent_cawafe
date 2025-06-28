from django.shortcuts import render, redirect
from inventario.models import Equipo, Estado_equipo
from usuarios.models import Usuario
from .models import HistorialEquipo
from collections import defaultdict

def vista_asociacion(request):
    equipos = []
    usuarios = Usuario.objects.all()
    historial_por_equipo = defaultdict(list)

    # Obtener filtros de búsqueda
    query_equipo = request.GET.get('equipo')
    query_usuario = request.GET.get('usuario')

    if query_equipo or query_usuario:
        equipos_filtrados = Equipo.objects.all()

        if query_equipo:
            equipos_filtrados = equipos_filtrados.filter(etiqueta__icontains=query_equipo)

        if query_usuario:
            equipos_filtrados = equipos_filtrados.filter(usuario_asignado__nombre_completo__icontains=query_usuario)

        equipos = equipos_filtrados

        for equipo in equipos:
            historial = HistorialEquipo.objects.filter(equipo=equipo).order_by('-fecha')[:5]
            historial_por_equipo[equipo.id] = historial

        equipos_con_historial = [(equipo, historial_por_equipo[equipo.id]) for equipo in equipos]
    else:
        equipos_con_historial = []

    if request.method == 'POST':
        equipo_id = request.POST.get('equipo_id')
        usuario_id = request.POST.get('empleado_id')
        estado_nombre = request.POST.get('estado')

        equipo = Equipo.objects.get(id=equipo_id)

        # Actualizar usuario asignado
        if estado_nombre.lower() == 'en_bodega':
            equipo.usuario_asignado = None
        elif usuario_id:
            nuevo_usuario = Usuario.objects.get(id=usuario_id)
            equipo.usuario_asignado = nuevo_usuario
        else:
            equipo.usuario_asignado = None

        # Actualizar estado
        estado_instancia = Estado_equipo.objects.get(nombre__iexact=estado_nombre)
        equipo.estado = estado_instancia
        equipo.save()

        # Registrar historial
        HistorialEquipo.objects.create(
            equipo=equipo,
            usuario_asignado=equipo.usuario_asignado,
            estado=estado_instancia,
            registrado_por=request.user
        )

        return redirect(f'/asociacion/?equipo={query_equipo or ""}&usuario={query_usuario or ""}')

    return render(request, 'asociacion/vista_asociacion.html', {
        'equipos': equipos,
        'empleados': usuarios,
        'query_equipo': query_equipo or '',
        'query_usuario': query_usuario or '',
        'equipos_con_historial': equipos_con_historial,
        'todos_los_equipos': Equipo.objects.all(),
    })


def historial_equipo(request, equipo_id):
    equipo = Equipo.objects.get(id=equipo_id)
    historial = HistorialEquipo.objects.filter(equipo=equipo).order_by('-fecha')

    return render(request, 'asociacion/historial_equipo.html', {
        'equipo': equipo,
        'historial': historial,
    })


def vista_lista_asociaciones(request):
    equipos = Equipo.objects.filter(usuario_asignado__isnull=False)

    for equipo in equipos:
        try:
            equipo.fecha_asignacion = HistorialEquipo.objects.filter(
                equipo=equipo
            ).latest('fecha').fecha
        except HistorialEquipo.DoesNotExist:
            equipo.fecha_asignacion = None

    return render(request, 'asociacion/lista_asociaciones.html', {
        'equipos': equipos,
    })
