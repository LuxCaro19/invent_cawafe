from django.shortcuts import render, get_object_or_404
from mantenciones.models import Tipo_mantencion, Tarea_tipo_mantencion

def detalle_tipo_mantencion(request, pk):
    tipo = get_object_or_404(Tipo_mantencion, pk=pk)

    # Tareas asociadas al tipo
    tareas_asociadas = tipo.tareas.all()

    # # Para más adelante: excluir tareas ya asociadas
    # tareas_disponibles = Tarea_tipo_mantencion.objects.exclude(id__in=tareas_asociadas.values_list('id', flat=True))

    context = {
        'tipo': tipo,
        'tareas_asociadas': tareas_asociadas,
        # 'tareas_disponibles': tareas_disponibles,
    }
    return render(request, 'mantenciones/detalle_tipo_mantencion.html', context)
