from django.shortcuts import render
from inventario.models.equipo import Equipo
from ventas.models.venta import Venta
from django.shortcuts import get_object_or_404, redirect
from inventario.models.estado_equipo import Estado_equipo
from inventario.models.equipo_historial import Equipo_historial
from django.views.decorators.http import require_POST




def listado_equipos(request):
    equipos = Equipo.objects.filter(estado_id=6)  # Filtra los equipos con estado "Activo"
    return render(request, 'listado_equipos.html', {'equipos': equipos})

def listado_equipos_rrhh(request):
    equipos = Equipo.objects.filter(estado_id=7)  # Filtra los equipos con estado "Pendiente RRHH"
    return render(request, 'listado_equipos_rrhh.html', {'equipos': equipos})

def listado_equipos_por_entregar(request):
    equipos = Equipo.objects.filter(estado_id=8)  # Filtra los equipos con estado "Pendiente RRHH"
    return render(request, 'listado_equipos_por_entregar.html', {'equipos': equipos})


def detalle_equipo(request, id):
    equipo = Equipo.objects.get(id=id)
    if request.method == 'POST':
        if 'eliminar' in request.POST:
            equipo.eliminar_equipo()
            equipos = Equipo.objects.filter(estado_id=6)
            return render(request, 'listado_equipos.html', {'equipos': equipos})
    return render(request, 'detalle_equipo.html', {'equipo': equipo})

def detalle_equipo_rrhh(request, id):
    equipo = get_object_or_404(Equipo, id=id)
    venta = Venta.objects.filter(id_equipo=equipo).first()

    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'aprobar':
            equipo.aprobar_por_rrhh()
        elif accion == 'rechazar':
            equipo.rechazar_por_rrhh()
        return redirect('listado_equipos_rrhh')

    return render(request, 'detalle_equipo_rrhh.html', {'equipo': equipo, 'venta': venta})


def detalleequipo_por_entregar(request, id):
    equipo = get_object_or_404(Equipo, id=id)
    venta = Venta.objects.filter(id_equipo=equipo).first()

    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'entregar':
            equipo.estado_id = 9  # ID del estado "Entregado"
            equipo.save()
            venta.flag_entregado = True
            venta.save()
            return redirect('listado_equipos_por_entregar')

    return render(request, 'detalle_equipo_por_entregar.html', {'equipo': equipo, 'venta': venta})

def comprar_equipo(request, id):
    equipo = get_object_or_404(Equipo, id=id)

    if request.method == 'POST':
        venta = Venta.objects.create(
            id_equipo=equipo,
            nombre_receptor='Juan Pérez',  # Podrás reemplazar esto luego por un input o usuario logueado
        )
        try:
            venta.procesar_compra()
            return render(request, 'compra_exitosa.html')
        except Exception as e:
            return render(request, 'comprar_equipo.html', {
                'equipo': equipo,
                'error': 'Ocurrió un error al procesar la compra. Intenta nuevamente.'
            })

    return render(request, 'comprar_equipo.html', {'equipo': equipo})


@require_POST
def confirmar_entrega(request, equipo_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)
    venta = Venta.objects.filter(id_equipo=equipo).first()

    if venta and venta.flag_aprobado_remuneraciones and not venta.flag_entregado:
        venta.flag_entregado = True
        venta.save()

        # Obtener los estados como instancias
        estado_anterior = Estado_equipo.objects.get(id=8)  # Pendiente Entrega
        estado_vendido = Estado_equipo.objects.get(id=9)   # Vendido

        # Actualizar estado del equipo
        equipo.estado = estado_vendido
        equipo.save()

        # Registrar en historial
        Equipo_historial.objects.create(
            equipo=equipo,
            estado_anterior=estado_anterior,
            nuevo_estado=estado_vendido
        )

    return redirect('listado_equipos_por_entregar')

def accion_rrhh_equipo(request, equipo_id, accion):
    equipo = get_object_or_404(Equipo, id=equipo_id)

    if accion == 'aprobar':
        equipo.aprobar_por_rrhh()
    elif accion == 'rechazar':
        equipo.rechazar_por_rrhh()

    return redirect('listado_equipos_rrhh')
