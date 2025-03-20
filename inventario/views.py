from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models.equipo import Equipo
from .models.modelo_equipo import Modelo_equipo
from django.shortcuts import get_list_or_404, get_object_or_404

# Create your views here.

def index(request):

    return HttpResponse("Index")

def listado_equipos(request):
    equipos = Equipo.objects.all()  # Obtiene todos los objetos de Equipo
    return render(request, 'listado_equipos.html', {'equipos': equipos})

def detalle_equipo(request, id):
    detalle = get_object_or_404(Equipo, id=id)
    return HttpResponse ('Equipo: %s' %detalle.etiqueta)