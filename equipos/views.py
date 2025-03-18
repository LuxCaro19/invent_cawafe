from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import ModeloEquipo,Equipos
from django.shortcuts import get_list_or_404, get_object_or_404

# Create your views here.

def index(request):

    return HttpResponse("Index")

def listado_equipos(request):
    equipos= list(Equipos.objects.values())
    return JsonResponse(equipos, safe=False)

def detalle_equipo(request, id):
    detalle = get_object_or_404(Equipos, id=id)
    return HttpResponse ('Equipo: %s' %detalle.etiqueta)