from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from mantenciones.models import Tipo_mantencion  # o el nombre correcto del modelo

def eliminar_tipo_mantencion(request, id):
    tipo = get_object_or_404(Tipo_mantencion, id=id)

    if request.method == 'POST':
        tipo.delete()
        messages.success(request, f"Tipo de mantención '{tipo.nombre}' eliminado correctamente.")
        return redirect('lista_tipos_mantencion')  # asegurate que este nombre esté definido en tu URL de listado

    # Opcional: redirige si alguien entra con GET
    return redirect('lista_tipos_mantencion')
