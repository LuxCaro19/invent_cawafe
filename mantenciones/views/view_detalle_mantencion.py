from django.shortcuts import render, get_object_or_404
from mantenciones.models import Mantencion
from datetime import date

def detalle_mantencion(request, pk):
    mantencion = get_object_or_404(
        Mantencion.objects.select_related(
            'equipo__modelo__tipo',
            'equipo__usuario_asignado__ubicacion',
            'tipo'
        ),
        pk=pk
    )

    tareas_tipo = mantencion.tipo.tareas.all() if mantencion.tipo else []
    registros = mantencion.registros.order_by('-fecha').all()

    # Precalcular tareas hechas y totales por registro
    for r in registros:
        tareas = r.tareas_realizadas.all()
        r.total_tareas = tareas.count()
        r.tareas_hechas = sum(1 for t in tareas if t.realizada)

    context = {
        "mantencion": mantencion,
        "equipo": mantencion.equipo,
        "tareas_tipo": tareas_tipo,
        "registros": registros,
        "today": date.today(),
    }

    return render(request, 'mantenciones/detalle_mantencion.html', context)
