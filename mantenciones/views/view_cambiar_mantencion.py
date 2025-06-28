from django.shortcuts import render, get_object_or_404, redirect
from mantenciones.models import Mantencion, Tipo_mantencion
from mantenciones.forms import Editar_mantencion
from django.http import JsonResponse

def cambiar_mantencion(request, pk):
    mantencion = get_object_or_404(Mantencion, pk=pk)
    form = Editar_mantencion(request.POST or None, instance=mantencion)

    tareas = []
    tipo = mantencion.tipo if mantencion.tipo_id else None

    if request.method == "POST":
        if form.is_valid():
            mantencion = form.save()
            return redirect('detalle_mantencion', pk=mantencion.pk)
        tipo_id = request.POST.get('tipo')
        if tipo_id:
            tipo = Tipo_mantencion.objects.filter(pk=tipo_id).first()

    elif request.method == "GET" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        tipo_id = request.GET.get("tipo_id")
        if tipo_id:
            tipo = get_object_or_404(Tipo_mantencion, pk=tipo_id)
            tareas = list(tipo.tareas.values("nombre"))
            return JsonResponse({"tareas": tareas})

    if tipo:
        tareas = tipo.tareas.all()

    context = {
        "mantencion": mantencion,
        "form": form,
        "tareas": tareas,
        "tipo": tipo,
    }
    return render(request, "mantenciones/editar_mantencion.html", context)
