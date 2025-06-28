from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from mantenciones.models import Mantencion

def eliminar_mantencion(request, mantencion_id):
    if request.method == "POST":
        mantencion = get_object_or_404(Mantencion, id=mantencion_id)
        mantencion.delete()
        messages.success(request, "Mantención eliminada correctamente.")
    return redirect('lista_mantenciones')
