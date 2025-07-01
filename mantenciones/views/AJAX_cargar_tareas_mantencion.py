from django.http import JsonResponse
from mantenciones.models import Tipo_mantencion

def obtener_tareas_por_tipo(request, tipo_id):
    tareas = Tipo_mantencion.objects.filter(pk=tipo_id).first()
    if not tareas:
        return JsonResponse([], safe=False)

    data = [{'descripcion': t.descripcion} for t in tareas.tareas.all()]
    return JsonResponse(data, safe=False)
