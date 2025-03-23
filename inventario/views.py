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
    return render(request, 'inventario/listados/listado_equipos.html', {'equipos': equipos})

def detalle_equipo(request, id):
    equipo = get_object_or_404(Equipo, id=id)

    if request.method == 'POST':
        if 'eliminar' in request.POST:
            equipo.delete()
            equipos = Equipo.objects.all()
            return render(request, 'inventario/listados/listado_equipos.html', {'equipos': equipos})
        else:
            form = EquipoForm(request.POST, instance=equipo)
            if form.is_valid():
                form.save()
                return redirect('detalle_equipo', id=equipo.id)
    else:
        form = EquipoForm(instance=equipo)

    return render(request, 'inventario/detalle/detalle_equipo.html', {'equipo': equipo, 'form': form})

def registrar_equipo(request):
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('detalle_equipo', id=Equipo.objects.latest('id').id)
    else:
        form = EquipoForm()
    return render(request, 'inventario/registro/registrar_equipo.html', {'equipo': Equipo,'form': form})

