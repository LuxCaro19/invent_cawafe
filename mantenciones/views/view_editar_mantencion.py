from django.shortcuts import render, get_object_or_404, redirect
from mantenciones.models import Mantencion, Registro_mantencion
from mantenciones.forms import Editar_mantencion

def editar_mantencion(request, pk):
    mantencion = get_object_or_404(Mantencion, pk=pk)
    form = Editar_mantencion(request.POST or None, instance=mantencion)
    if form.is_valid():
        form.save()
        return redirect('detalle_mantencion', pk=mantencion.pk)
    return render(request, 'mantenciones/editar_mantencion.html', {'form': form, 'mantencion': mantencion})