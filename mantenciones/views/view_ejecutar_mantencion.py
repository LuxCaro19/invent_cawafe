from django.shortcuts import render, get_object_or_404, redirect
from mantenciones.models import Mantencion
from mantenciones.forms import Ejecutar_Mantencion

def nueva_mantencion_registro(request, mantencion_id):
    mantencion = get_object_or_404(Mantencion, pk=mantencion_id)
    tareas = mantencion.tipo.tareas.all() if mantencion.tipo else []

    if request.method == 'POST':
        form = Ejecutar_Mantencion(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.mantencion = mantencion
            registro.tipo = mantencion.tipo.nombre if mantencion.tipo else 'Desconocido'
            registro.responsable = request.user  # <<< aquí va el usuario actual
            registro.save()

            tareas_realizadas = request.POST.getlist('tareas_realizadas')
            for descripcion in tareas_realizadas:
                registro.tareas_realizadas.create(
                    descripcion=descripcion,
                    realizada=True
                )

            return redirect('detalle_mantencion', pk=mantencion.id)
    else:
        form = Ejecutar_Mantencion()

    return render(request, 'mantenciones/ejecutar_mantencion.html', {
        'form': form,
        'mantencion': mantencion,
        'tareas': tareas,
        'usuario': request.user,  # <<< lo pasamos al template
    })
