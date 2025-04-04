from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Equipo, Equipo_historial
from .models.modelo_equipo import Modelo_equipo
from django.shortcuts import get_list_or_404, get_object_or_404,redirect
from .forms.equipo_form import EquipoForm
from .forms.modelo_equipo_form import Modelo_equipoForm

# Create your views here.

def index(request):

    return HttpResponse("Index")

# Vista de listados
def listado_equipos(request):
    equipos = Equipo.objects.all()  # Obtiene todos los objetos de Equipo
    return render(request, 'inventario/listados/listado_equipos.html', {'equipos': equipos})

def listado_modelo_equipo(request):
    modelos = Modelo_equipo.objects.all()  # Obtiene todos los objetos de Equipo
    return render(request, 'inventario/listados/listado_modelo_equipos.html', {'modelos': modelos})

##############################

##############################
# Vista de detalles

def detalle_equipo(request, id):
    equipo = get_object_or_404(Equipo, id=id)

    if request.method == 'POST':
        if 'eliminar' in request.POST:
            equipo.eliminar_equipo()
            equipos = Equipo.objects.all()
            return render(request, 'inventario/listados/listado_equipos.html', {'equipos': equipos})
        else:
            form = EquipoForm(request.POST, instance=equipo)
            if form.is_valid():
                equipo.modificar_equipo(form)
                return redirect('detalle_equipo', id=equipo.id)
    else:
        form = EquipoForm(instance=equipo)

    historial = Equipo_historial.objects.filter(equipo=equipo).order_by('-fecha')

    return render(request, 'inventario/detalle/detalle_equipo.html', {'equipo': equipo, 'form': form, 'historial': historial})



def detalle_modelo_equipo(request, id):
    modelo = get_object_or_404(Modelo_equipo, id=id)

    if request.method == 'POST':
        if 'eliminar' in request.POST:
            modelo.eliminar_modelo()
            modelos = Modelo_equipo.objects.all()
            return render(request, 'inventario/listados/listado_modelo_equipos.html', {'modelos': modelos})
        else:
            form = Modelo_equipoForm(request.POST, instance=modelo)
            if form.is_valid():
                modelo.modificar_modelo(form)
                return redirect('detalle_modelo_equipo', id=modelo.id)
    else:
        form = Modelo_equipoForm(instance=modelo)

    return render(request, 'inventario/detalle/detalle_modelo_equipo.html', {'modelo': modelo, 'form': form})

##############################

##############################
# Vista de formularios de registro 
def registrar_equipo(request):
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('detalle_equipo', id=Equipo.objects.latest('id').id)
    else:
        form = EquipoForm()
    return render(request, 'inventario/registro/registrar_equipo.html', {'equipo': Equipo,'form': form})


def registrar_modelo_equipo(request):
    if request.method == 'POST':
        form = Modelo_equipoForm(request.POST)
        if form.is_valid():
            form.save()
            #return redirect('detalle_modelo_equipo', id=Modelo_equipo.objects.latest('id').id)
            modelos = Modelo_equipo.objects.all()
            return render(request, 'inventario/listados/listado_modelo_equipos.html', {'modelos': modelos,'form': form})
    else:
        form = Modelo_equipoForm()
    return render(request, 'inventario/registro/registrar_modelo.html', {'modelo_equipo': Modelo_equipo,'form': form})