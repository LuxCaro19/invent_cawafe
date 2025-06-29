from django.shortcuts import render, get_object_or_404, redirect
from mantenciones.models import Mantencion, Tipo_mantencion
from mantenciones.forms import Editar_mantencion

def editar_mantencion(request, pk):
    mantencion = get_object_or_404(Mantencion, pk=pk)
    form = Editar_mantencion(request.POST or None, instance=mantencion)

    # Si se seleccionó un tipo en el POST, usamos ese para mostrar tareas
    tipo_seleccionado = None
    tareas = []

    if request.method == 'POST':
        if request.POST.get('tipo'):
            try:
                tipo_seleccionado = Tipo_mantencion.objects.get(pk=request.POST.get('tipo'))
                tareas = tipo_seleccionado.tareas.all()
            except Tipo_mantencion.DoesNotExist:
                tareas = []
    else:
        if mantencion.tipo:
            tareas = mantencion.tipo.tareas.all()

    if form.is_valid():
        form.save()
        return redirect('detalle_mantencion', pk=mantencion.pk)

    return render(request, 'mantenciones/editar_mantencion.html', {
        'form': form,
        'mantencion': mantencion,
        'tareas': tareas,
        'tipo': tipo_seleccionado or mantencion.tipo
    })
