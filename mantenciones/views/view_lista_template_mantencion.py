from django.shortcuts import render
from mantenciones.models import Tipo_mantencion
from inventario.models import Sistema_operativo, Modelo_tipo

def lista_template_mantencion(request):
    sistemas_operativos = Sistema_operativo.objects.all()
    tipos_equipo = Modelo_tipo.objects.all()

    # Todos los tipos de mantención, con opción de excluir algunos
    excluir_ids = request.GET.getlist('excluir', [])
    queryset_tipos = Tipo_mantencion.objects.all()
    if excluir_ids:
        queryset_tipos = queryset_tipos.exclude(id__in=excluir_ids)

    context = {
        'sistemas_operativos': sistemas_operativos,
        'tipos_equipo': tipos_equipo,
        'tipos_mantencion': queryset_tipos,
    }

    return render(request, 'mantenciones/lista_template_mantencion.html', context)
