from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from mantenciones.models import Mantencion, Tipo_mantencion
from mantenciones.forms import Editar_mantencion

def editar_mantencion(request, pk):
    mantencion = get_object_or_404(Mantencion, pk=pk)
    form = Editar_mantencion(request.POST or None, instance=mantencion)

    tipo_seleccionado = mantencion.tipo
    tareas = tipo_seleccionado.tareas.all() if tipo_seleccionado else []

    if request.method == 'POST':
        mostrar_tareas = request.POST.get('mostrar_tareas') == '1'

        if request.POST.get('tipo'):
            try:
                tipo_seleccionado = Tipo_mantencion.objects.get(pk=request.POST.get('tipo'))
                tareas = tipo_seleccionado.tareas.all()
            except Tipo_mantencion.DoesNotExist:
                tareas = []

        if not mostrar_tareas and form.is_valid():
            form.save()
            return redirect('detalle_mantencion', pk=mantencion.pk)

    return render(request, 'mantenciones/editar_mantencion.html', {
        'form': form,
        'mantencion': mantencion,
        'tareas': tareas,
        'tipo': tipo_seleccionado,
    })


# 👇 NUEVA FUNCIÓN para usar con JavaScript
def obtener_tareas_tipo(request, pk):
    try:
        tipo = Tipo_mantencion.objects.get(pk=pk)
        tareas = list(tipo.tareas.values('descripcion'))
        return JsonResponse(tareas, safe=False)
    except Tipo_mantencion.DoesNotExist:
        return JsonResponse([], safe=False)
