from django.shortcuts import render, get_object_or_404, redirect
from mantenciones.models import Mantencion, Registro_mantencion

def nueva_mantencion_registro(request, mantencion_id):
    mantencion = get_object_or_404(
        Mantencion.objects.select_related(
            'equipo__modelo__tipo',
            'equipo__usuario_asignado__ubicacion',
            'tipo'
        ),
        pk=mantencion_id
    )
    tareas = mantencion.tipo.tareas.all() if mantencion.tipo else []

    if request.method == 'POST':
        observaciones = request.POST.get('observaciones', '').strip()
        tareas_realizadas = request.POST.getlist('tareas_realizadas')

        registro = Registro_mantencion.objects.create(
            mantencion=mantencion,
            tipo=mantencion.tipo.nombre if mantencion.tipo else 'Desconocido',
            responsable=request.user,
            ubicacion=(
                mantencion.equipo.usuario_asignado.ubicacion
                if mantencion.equipo.usuario_asignado and mantencion.equipo.usuario_asignado.ubicacion
                else ''
            ),
            observaciones=observaciones
        )

        for tarea in tareas:
            registro.tareas_realizadas.create(
                tarea=tarea,
                descripcion=tarea.descripcion,
                realizada=(tarea.descripcion in tareas_realizadas)
            )

        return redirect('detalle_mantencion', pk=mantencion.id)

    return render(request, 'mantenciones/ejecutar_mantencion.html', {
        'mantencion': mantencion,
        'tareas': tareas,
        'usuario': request.user,
    })
