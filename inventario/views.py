from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models.equipo import Equipo
from .models.modelo_equipo import Modelo_equipo
from django.shortcuts import get_list_or_404, get_object_or_404,redirect
from .forms.equipo_form import EquipoForm

# Create your views here.

def index(request):

    return HttpResponse("Index")

def listado_equipos(request):
    equipos = Equipo.objects.all()  # Obtiene todos los objetos de Equipo
    return render(request, 'inventario/listado_equipos.html', {'equipos': equipos})

def detalle_equipo(request, id):
    equipo = get_object_or_404(Equipo, id=id)
    form = EquipoForm(instance=equipo)
    if request.method == 'POST':
        form = EquipoForm(request.POST, instance=equipo)
        if form.is_valid():
            form.save()
            return redirect('detalle_equipo', id=equipo.id)
        
    return render(request, 'inventario/detalle_equipo.html', {'equipo': equipo, 'form': form})

