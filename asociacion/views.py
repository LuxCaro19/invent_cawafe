from django.shortcuts import render, redirect
from inventario.models import Equipo, Estado_equipo
from usuarios.models import Usuario
from .models import HistorialEquipo
from collections import defaultdict
from django.http import JsonResponse
from django.db.models import Q
from inventario.models import Equipo, Estado_equipo, Ubicacion  # ← agrega Ubicacion aquí
from django.urls import reverse
from django.http import HttpResponseRedirect
from urllib.parse import urlencode
from .utils.pdf_comodato import generar_pdf_comodato, generar_pdf_recepcion
from django.http import HttpResponse
from django.utils import timezone

def vista_asociacion(request):
    query_equipo = request.GET.get('equipo', '')
    query_usuario = request.GET.get('usuario', '')

    if request.method == 'POST':
        equipo_id = request.POST.get('equipo_id')
        usuario_id = request.POST.get('usuario_id')
        a_bodega = request.POST.get('bodega') == 'on'

        equipo = Equipo.objects.get(id=equipo_id)
        usuario_anterior = equipo.usuario_asignado

        if a_bodega:
            equipo.usuario_asignado = None
            equipo.en_bodega = True
            equipo.estado = Estado_equipo.objects.get(nombre__iexact="Operativo")
            equipo.ubicacion = Ubicacion.objects.get(nombre__iexact="En Bodega")
        else:
            equipo.en_bodega = False
            if usuario_id:
                nuevo_usuario = Usuario.objects.get(id=usuario_id)
                equipo.usuario_asignado = nuevo_usuario
                equipo.estado = Estado_equipo.objects.get(nombre__iexact="Asignado")
                equipo.ubicacion = None


            else:
                equipo.usuario_asignado = None


        equipo.save()

        ultimo_historial = HistorialEquipo.objects.filter(equipo=equipo).order_by('-fecha').first()

        if (
            not ultimo_historial or
            ultimo_historial.usuario_asignado != equipo.usuario_asignado or
            ultimo_historial.estado != equipo.estado
        ):
            HistorialEquipo.objects.create(
                equipo=equipo,
                usuario_asignado=equipo.usuario_asignado,
                estado=equipo.estado,
                registrado_por=request.user
            )

        # Redirecciona SIN repetir la lógica
        params = {}
        if query_equipo:
            params['equipo'] = query_equipo
        if query_usuario:
            params['usuario'] = query_usuario

        url = reverse('vista_asociacion')
        if params:
            url += '?' + urlencode(params)

        

        # Genera el PDF de comodato si se asignó un usuario
        # Preparar contexto para PDF

        if not a_bodega and usuario_id:
            nuevo_usuario = Usuario.objects.get(id=usuario_id)

            contexto = {
                'fecha': timezone.now().strftime('%d de %B de %Y'),
                'equipo': equipo.etiqueta,
                'nombre_usuario': nuevo_usuario.nombre_completo,
                'rut_usuario': nuevo_usuario.rut,
                'modelo': equipo.modelo.nombre,
                'marca': equipo.modelo.marca.marca,
                'imei': equipo.imei or '—',
                'estado': equipo.estado.nombre,
                'valor': equipo.modelo.precio,
            }

            pdf_file = generar_pdf_comodato(contexto)
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="Comodato_{equipo.etiqueta}.pdf"'
            return response
        else:
            entregado_por = request.POST.get('entregado_por', 'No especificado')
            estado_recepcion = request.POST.get('estado_recepcion', 'Sin información')

            contexto_pdf_recepcion = {
                'equipo': equipo,
                'fecha': timezone.now().strftime('%d de %B de %Y'),
                'usuario_asignado': usuario_anterior,
                'entregado_por': entregado_por,
                'estado_recepcion': estado_recepcion,
                'registrado_por': request.user.nombre_completo,
            }

            pdf_file = generar_pdf_recepcion(contexto_pdf_recepcion)
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="Recepcion_{equipo.etiqueta}.pdf"'
            return response


    # Solo ejecuta la lógica GET después de manejar el POST
    filtros = Q()
    if query_equipo:
        filtros &= Q(etiqueta__icontains=query_equipo)
    if query_usuario:
        filtros &= Q(usuario_asignado__nombre_completo__icontains=query_usuario)

    equipos = Equipo.objects.filter(filtros).distinct() if filtros else []
    historial_por_equipo = defaultdict(list)

    for equipo in equipos:
        historial = HistorialEquipo.objects.filter(equipo=equipo).order_by('-fecha')[:5]
        historial_por_equipo[equipo.id] = historial

    equipos_con_historial = [(equipo, historial_por_equipo[equipo.id]) for equipo in equipos]

    return render(request, 'asociacion/vista_asociacion.html', {
        'usuarios': Usuario.objects.all(),
        'estados': Estado_equipo.objects.all(),
        'equipos_con_historial': equipos_con_historial,
        'query_equipo': query_equipo,
        'query_usuario': query_usuario,
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

def buscar_equipo_asociar(request):
    if request.method == 'POST':
        etiqueta = request.POST.get('etiqueta', '').strip()
        if Equipo.objects.filter(etiqueta=etiqueta).exists():
            return redirect(f'/asociacion/?equipo={etiqueta}')
        else:
            return render(request, 'asociacion/buscar_equipo.html', {
                'error': 'No se encontró un equipo con esa etiqueta.'
            })

    return render(request, 'asociacion/buscar_equipo.html')