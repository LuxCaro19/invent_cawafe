from django.shortcuts import render,get_object_or_404
from mantenciones.models import Mantencion
from datetime import date

def detalle_mantencion(request, pk):
    mantencion = get_object_or_404(Mantencion.objects.select_related(
        'equipo__modelo__tipo', 'tipo'), pk=pk)
    
    tareas_tipo = mantencion.tipo.tareas.all() if mantencion.tipo else []
    registros = mantencion.registros.order_by('-fecha').all()

    context = {
        "mantencion": mantencion,
        "tareas_tipo": tareas_tipo,
        "registros": registros,
        "today": date.today(),
    }

    return render(request, 'mantenciones/detalle_mantencion.html', context)
