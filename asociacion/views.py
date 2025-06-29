from django.shortcuts import render, redirect
from inventario.models import Equipo, Estado_equipo
from usuarios.models import Usuario
from .models import HistorialEquipo
from collections import defaultdict
from django.http import JsonResponse
from django.db.models import Q
from inventario.models import Equipo, Estado_equipo, Ubicacion  # ← agrega Ubicacion aquí


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
        usuario_id = request.POST.get('usuario_id')
        a_bodega = request.POST.get('bodega') == 'on'

        equipo = Equipo.objects.get(id=equipo_id)

        if a_bodega:
            equipo.usuario_asignado = None
            equipo.en_bodega = True

            # Estado: Operativo
            estado_operativo = Estado_equipo.objects.get(nombre__iexact="Operativo")
            equipo.estado = estado_operativo

            # Ubicación: En Bodega
            ubicacion_bodega = Ubicacion.objects.get(nombre__iexact="En Bodega")
            equipo.ubicacion = ubicacion_bodega

        else:
            equipo.en_bodega = False
            if usuario_id:
                nuevo_usuario = Usuario.objects.get(id=usuario_id)
                equipo.usuario_asignado = nuevo_usuario

                # Estado: Asignado
                estado_asignado = Estado_equipo.objects.get(nombre__iexact="Asignado")
                equipo.estado = estado_asignado

                # Borrar ubicación (opcional o puedes poner una por defecto)
                equipo.ubicacion = None
            else:
                equipo.usuario_asignado = None

        equipo.save()

        # Registrar historial
        HistorialEquipo.objects.create(
            equipo=equipo,
            usuario_asignado=equipo.usuario_asignado,
            estado=equipo.estado,
            registrado_por=request.user
        )

        return redirect(f'/asociacion/?equipo={query_equipo or ""}&usuario={query_usuario or ""}')


    # Asegúrate de enviar los estados si necesitas renderizar el dropdown
    estados = Estado_equipo.objects.all()

    return render(request, 'asociacion/vista_asociacion.html', {
        'equipos': equipos,
        'usuarios': usuarios,
        'query_equipo': query_equipo or '',
        'query_usuario': query_usuario or '',
        'equipos_con_historial': equipos_con_historial,
        'todos_los_equipos': Equipo.objects.all(),
        'estados': estados,
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

def autocomplete_equipos(request):
    term = request.GET.get('term', '')
    qs = Equipo.objects.filter(etiqueta__icontains=term)
    etiquetas = list(qs.values_list('etiqueta', flat=True)[:10])  # máximo 10 resultados
    return JsonResponse(etiquetas, safe=False)
    
def autocomplete_usuarios(request):
    term = request.GET.get('term', '')
    usuarios = Usuario.objects.filter(nombre_completo__icontains=term)[:10]
    results = [{"label": u.nombre_completo, "value": u.nombre_completo} for u in usuarios]
    return JsonResponse(results, safe=False)