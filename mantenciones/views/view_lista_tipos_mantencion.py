from django.shortcuts import render
from mantenciones.models import Tipo_mantencion  # Asegúrate que el modelo esté bien escrito

def lista_tipos_mantencion(request):
    tipos = Tipo_mantencion.objects.select_related('modelo_tipo', 'sistema_operativo').all()
    return render(request, 'mantenciones/lista_tipos_mantencion.html', {'tipos': tipos})
