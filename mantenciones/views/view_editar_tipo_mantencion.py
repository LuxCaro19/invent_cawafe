from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from mantenciones.models import Tipo_mantencion, Tarea_tipo_mantencion
from mantenciones.forms.editar_tipo_mantencion import TipoMantencionEditarForm


def editar_tipo_mantencion(request, id):
    tipo = get_object_or_404(Tipo_mantencion, id=id)
    tareas_asociadas = tipo.tareas.all()
    tareas_disponibles = Tarea_tipo_mantencion.objects.exclude(id__in=tareas_asociadas)

    if request.method == "POST":
        form = TipoMantencionEditarForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            return redirect("lista_tipos_mantencion")  # ← redirección corregida
    else:
        form = TipoMantencionEditarForm(instance=tipo)

    return render(request, "mantenciones/editar_tipo_mantencion.html", {
        "form": form,
        "tareas_asociadas": tareas_asociadas,
        "tareas_disponibles": tareas_disponibles,
        "tipo": tipo,
    })



@require_POST
def agregar_tarea_tipo_mantencion(request, tipo_id):
    tipo = get_object_or_404(Tipo_mantencion, id=tipo_id)
    descripcion = request.POST.get("nueva_tarea_texto")

    if descripcion:
        Tarea_tipo_mantencion.objects.create(tipo=tipo, descripcion=descripcion)

    return redirect("editar_tipo_mantencion", id=tipo_id)




@require_POST
def eliminar_tarea_tipo_mantencion(request, tipo_id, tarea_id):
    tipo = get_object_or_404(Tipo_mantencion, id=tipo_id)
    tarea = get_object_or_404(Tarea_tipo_mantencion, id=tarea_id, tipo=tipo)
    tarea.delete()  # Elimina la instancia asociada
    return redirect("editar_tipo_mantencion", id=tipo_id)
