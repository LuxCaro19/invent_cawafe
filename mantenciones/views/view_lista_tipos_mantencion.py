from django.shortcuts import render
from mantenciones.models import Tipo_mantencion

def lista_tipos_mantencion(request):
    tipos = Tipo_mantencion.objects.select_related('modelo_tipo', 'sistema_operativo') \
                                    .exclude(nombre__iexact="Creación")  # Ignora el tipo con nombre "Creación"
    return render(request, 'mantenciones/lista_tipos_mantencion.html', {'tipos': tipos})
