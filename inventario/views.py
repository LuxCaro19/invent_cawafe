from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Equipo, Equipo_historial
from .models.modelo_equipo import Modelo_equipo
from .models.modelo_marca import Modelo_marca
from .models.modelo_tipo import Modelo_tipo
from .models.estado_equipo import Estado_equipo
from django.shortcuts import get_list_or_404, get_object_or_404,redirect
from .forms.equipo_form import EquipoForm
from .forms.modelo_equipo_form import Modelo_equipoForm
from .forms.modelo_marca_form import Modelo_marcaForm
from .forms.tipo_equipo_form import Tipo_equipoForm
from .models.procesador import Procesador
from .models.sistema_operativo import Sistema_operativo
from .forms.procesador_form import ProcesadorForm
from .forms.so_form import SoForm
from .forms.estado_equipo_form import Estado_equipoForm
from django.http import JsonResponse
from django.urls import reverse 
from django.utils import timezone

# Create your views here.

def index(request):

    return HttpResponse("Index")

# Vista de listados
from django.db.models import F
from collections import defaultdict
from .models import Equipo

def listado_equipos(request):
    equipos = Equipo.objects.select_related(
        "modelo__marca", "modelo__tipo", "procesador", "sistema_operativo",
        "estado", "usuario_asignado", "usuario_asignado__ubicacion", "ubicacion"
    )

    buscar = request.GET.get("buscar", "").strip()
    campo = request.GET.get("campo", "")
    agrupar = request.GET.get("agrupar", "")

    if buscar and campo:
        if campo == "etiqueta":
            equipos = equipos.filter(etiqueta__icontains=buscar)
        elif campo == "modelo":
            equipos = equipos.filter(modelo__nombre__icontains=buscar)
        elif campo == "procesador":
            equipos = equipos.filter(procesador__nombre__icontains=buscar)

    grupos = defaultdict(list)

    if agrupar == "sistema_operativo":
        for equipo in equipos:
            clave = equipo.sistema_operativo.nombre if equipo.sistema_operativo else "Sin S.O."
            grupos[clave].append(equipo)
    elif agrupar == "marca":
        for equipo in equipos:
            clave = equipo.modelo.marca.marca if equipo.modelo and equipo.modelo.marca else "Sin Marca"
            grupos[clave].append(equipo)
    elif agrupar == "modelo":
        for equipo in equipos:
            clave = equipo.modelo.nombre if equipo.modelo else "Sin Modelo"
            grupos[clave].append(equipo)
    elif agrupar == "procesador":
        for equipo in equipos:
            clave = equipo.procesador.nombre if equipo.procesador else "Sin Procesador"
            grupos[clave].append(equipo)
    elif agrupar == "estado":
        for equipo in equipos:
            clave = equipo.estado.nombre if equipo.estado else "Sin Estado"
            grupos[clave].append(equipo)
    elif agrupar == "usuario":
        for equipo in equipos:
            clave = equipo.usuario_asignado.nombre_completo if equipo.usuario_asignado else "No asignado"
            grupos[clave].append(equipo)
    elif agrupar == "ubicacion":
        for equipo in equipos:
            if equipo.en_bodega and equipo.ubicacion:
                clave = equipo.ubicacion.nombre
            elif equipo.usuario_asignado and equipo.usuario_asignado.ubicacion:
                clave = equipo.usuario_asignado.ubicacion.nombre
            else:
                clave = "Sin ubicación"
            grupos[clave].append(equipo)
    else:
        grupos["Todos"] = equipos

    return render(request, "inventario/listados/listado_equipos.html", {
        "grupos": dict(grupos),
        "filtro_busqueda": buscar,
        "campo": campo,
        "agrupar": agrupar,
    })

def listado_modelo_equipo(request):
    buscar = request.GET.get("buscar", "").strip()
    agrupar = request.GET.get("agrupar", "")

    modelos = Modelo_equipo.objects.select_related("marca", "tipo").all()

    if buscar:
        modelos = modelos.filter(
            Q(nombre__icontains=buscar) |
            Q(marca__marca__icontains=buscar)
        )

    grupos = defaultdict(list)

    if agrupar == "marca":
        for modelo in modelos:
            clave = modelo.marca.marca if modelo.marca else "Sin Marca"
            grupos[clave].append(modelo)
    elif agrupar == "tipo":
        for modelo in modelos:
            clave = modelo.tipo.tipo if modelo.tipo else "Sin Tipo"
            grupos[clave].append(modelo)
    else:
        grupos["Todos"] = modelos

    return render(request, 'inventario/listados/listado_modelo_equipos.html', {
        'grupos': dict(grupos),
        'filtro_busqueda': buscar,
        'agrupar': agrupar,
    })

def listado_marcas(request):
    buscar = request.GET.get("buscar", "").strip()
    marcas = Modelo_marca.objects.all()

    if buscar:
        marcas = marcas.filter(marca__icontains=buscar)

    return render(request, 'inventario/listados/listado_marcas.html', {
        'marcas': marcas,
        'filtro_busqueda': buscar,
    })

def listado_tipo_equipos(request):
    buscar = request.GET.get("buscar", "").strip()
    tipos = Modelo_tipo.objects.all()

    if buscar:
        tipos = tipos.filter(tipo__icontains=buscar)

    return render(request, 'inventario/listados/listado_tipo_equipos.html', {
        'tipos': tipos,
        'filtro_busqueda': buscar,
    })

def listado_procesadores(request):
    buscar = request.GET.get("buscar", "").strip()
    agrupar = request.GET.get("agrupar", "")

    procesadores = Procesador.objects.select_related("marca").all()

    if buscar:
        procesadores = procesadores.filter(
            Q(nombre__icontains=buscar) |
            Q(marca__marca__icontains=buscar)
        )

    grupos = defaultdict(list)

    if agrupar == "marca":
        for proc in procesadores:
            clave = proc.marca.marca if proc.marca else "Sin Marca"
            grupos[clave].append(proc)
    else:
        grupos["Todos"] = procesadores

    return render(request, 'inventario/listados/listado_procesador.html', {
        'grupos': dict(grupos),
        'filtro_busqueda': buscar,
        'agrupar': agrupar,
    })

def listado_sistemas_operativos(request):
    buscar = request.GET.get("buscar", "").strip()
    agrupar = request.GET.get("agrupar", "")

    sistemas_operativos = Sistema_operativo.objects.select_related("marca").all()

    if buscar:
        sistemas_operativos = sistemas_operativos.filter(
            Q(nombre__icontains=buscar) |
            Q(marca__marca__icontains=buscar)
        )

    grupos = defaultdict(list)

    if agrupar == "marca":
        for so in sistemas_operativos:
            clave = so.marca.marca if so.marca else "Sin Marca"
            grupos[clave].append(so)
    else:
        grupos["Todos"] = sistemas_operativos

    return render(request, 'inventario/listados/listado_so.html', {
        'sistemas_operativos': sistemas_operativos,
        'grupos': dict(grupos),
        'filtro_busqueda': buscar,
        'agrupar': agrupar,
    })

def listado_estado_equipos(request):
    buscar = request.GET.get("buscar", "").strip()

    estados = Estado_equipo.objects.all()
    if buscar:
        estados = estados.filter(nombre__icontains=buscar)

    return render(request, 'inventario/listados/listado_estados.html', {
        'estados': estados,
        'filtro_busqueda': buscar,
    })

##############################

##############################
# Vista de detalles
 # Asegúrate de tener este import arriba

def detalle_equipo(request, id):
    equipo = get_object_or_404(Equipo, id=id)
    historial = Equipo_historial.objects.filter(equipo=equipo).order_by('-fecha')

    if request.method == 'POST':
        # Lógica de eliminación
        if 'eliminar' in request.POST:
            equipo.delete()
            return redirect('listado_equipos')  # Ajusta según la vista de destino

        # Lógica de edición
        form = EquipoForm(request.POST, instance=equipo)
        if form.is_valid():
            cambios = []
            equipo_original = Equipo.objects.get(pk=equipo.pk)
            estado_anterior = equipo_original.estado

            for campo, nuevo_valor in form.cleaned_data.items():
                valor_actual = getattr(equipo_original, campo)

                if hasattr(valor_actual, 'id') and hasattr(nuevo_valor, 'id'):
                    if valor_actual.id != nuevo_valor.id:
                        cambios.append(f"{campo}: {valor_actual} → {nuevo_valor}")
                        setattr(equipo, campo, nuevo_valor)
                elif valor_actual != nuevo_valor:
                    cambios.append(f"{campo}: {valor_actual} → {nuevo_valor}")
                    setattr(equipo, campo, nuevo_valor)

            equipo.save()

            if cambios:
                observaciones = f"Modificado por {request.user}\n" + "\n".join(cambios)
                Equipo_historial.objects.create(
                    equipo=equipo,
                    fecha=timezone.now(),
                    estado_anterior=estado_anterior,
                    nuevo_estado=equipo.estado,
                    observaciones=observaciones
                )

            return redirect('detalle_equipo', id=equipo.id)

    else:
        form = EquipoForm(instance=equipo)

    return render(request, 'inventario/detalle/detalle_equipo.html', {
        'equipo': equipo,
        'form': form,
        'historial': historial,
        'detalle_equipo_url': reverse('detalle_equipo', args=[equipo.id])
    })

def detalle_modelo_equipo(request, id):
    modelo = get_object_or_404(Modelo_equipo, id=id)

    if request.method == 'POST':
        if 'eliminar' in request.POST:
            modelo.eliminar_modelo()
            return redirect('listado_modelo_equipos')  # redirige a la vista real de lista
        else:
            form = Modelo_equipoForm(request.POST, instance=modelo)
            if form.is_valid():
                modelo.modificar_modelo(form)
                return redirect('detalle_modelo_equipo', id=modelo.id)
    else:
        form = Modelo_equipoForm(instance=modelo)

    return render(request, 'inventario/detalle/detalle_modelo_equipo.html', {
        'modelo': modelo,
        'form': form
    })

def detalle_marca_equipo(request, id):
    marca = get_object_or_404(Modelo_marca, id=id)

    if request.method == 'POST':
        if 'eliminar' in request.POST:
            marca.eliminar_marca()
            return redirect('listado_marcas')  # redirige a la vista real de listado
        else:
            form = Modelo_marcaForm(request.POST, instance=marca)
            if form.is_valid():
                marca.modificar_marca(form)
                return redirect('detalle_marca', id=marca.id)
    else:
        form = Modelo_marcaForm(instance=marca)

    return render(request, 'inventario/detalle/detalle_marca.html', {
        'marca': marca,
        'form': form
    })

def detalle_tipo_equipo(request, id):
    tipo = get_object_or_404(Modelo_tipo, id=id)

    if request.method == 'POST':
        if 'eliminar' in request.POST:
            tipo.eliminar_tipo()
            return redirect('listado_tipo_equipos')  # redirige a la vista real de listado
        else:
            form = Tipo_equipoForm(request.POST, instance=tipo)
            if form.is_valid():
                tipo.modificar_tipo(form)
                return redirect('detalle_tipo_equipo', id=tipo.id)
    else:
        form = Tipo_equipoForm(instance=tipo)

    return render(request, 'inventario/detalle/detalle_tipo_equipo.html', {
        'tipo': tipo,
        'form': form
    })

def detalle_procesador(request, id):
    procesador = get_object_or_404(Procesador, id=id)

    if request.method == 'POST':
        if 'eliminar' in request.POST:
            procesador.delete()
            return redirect('listado_procesadores')
        else:
            form = ProcesadorForm(request.POST, instance=procesador)
            if form.is_valid():
                form.save()
                return redirect('detalle_procesador', id=procesador.id)
    else:
        form = ProcesadorForm(instance=procesador)

    return render(request, 'inventario/detalle/detalle_procesador.html', {
        'procesador': procesador,
        'form': form
    })

def detalle_sistema_operativo(request, id):
    so = get_object_or_404(Sistema_operativo, id=id)

    if request.method == 'POST':
        if 'eliminar' in request.POST:
            so.delete()
            return redirect('listado_sistemas_operativos')
        else:
            form = SoForm(request.POST, instance=so)
            if form.is_valid():
                form.save()
                return redirect('detalle_so', id=so.id)
    else:
        form = SoForm(instance=so)

    return render(request, 'inventario/detalle/detalle_so.html', {
        'so': so,
        'form': form
    })

def detalle_estado_equipo(request, id):
    estado = get_object_or_404(Estado_equipo, id=id)

    if request.method == 'POST':
        if 'eliminar' in request.POST:
            estado.delete()
            return redirect('listado_estados')
        else:
            form = Estado_equipoForm(request.POST, instance=estado)
            if form.is_valid():
                form.save()
                return redirect('detalle_estado', id=estado.id)
    else:
        form = Estado_equipoForm(instance=estado)

    return render(request, 'inventario/detalle/detalle_estado.html', {
        'estado': estado,
        'form': form
    })

##############################

##############################
# Vista de formularios de registro 
def registrar_equipo(request):
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            equipo = form.save()  # Guardamos el equipo

            # Registrar en historial
            from django.utils import timezone
            from .models import Equipo_historial

            if request.user.is_authenticated:
                creador = getattr(request.user, 'nombre_completo', str(request.user))
            else:
                creador = 'desconocido'

            observaciones = f"Equipo creado por {creador}"

            Equipo_historial.objects.create(
                equipo=equipo,
                fecha=timezone.now(),
                estado_anterior=None,
                nuevo_estado=equipo.estado,
                observaciones=observaciones
            )

            return redirect('detalle_equipo', id=equipo.id)
    else:
        form = EquipoForm()
    return render(request, 'inventario/registro/registrar_equipo.html', {'equipo': Equipo, 'form': form})

def registrar_modelo_equipo(request):
    if request.method == 'POST':
        form = Modelo_equipoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado_modelo_equipos')  # Asegúrate que esta es la URL correcta
    else:
        form = Modelo_equipoForm()

    return render(request, 'inventario/registro/registrar_modelo.html', {'form': form})

def registrar_marca_equipo(request):
    if request.method == 'POST':
        form = Modelo_marcaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado_marcas')
    else:
        form = Modelo_marcaForm()

    return render(request, 'inventario/registro/registrar_marca.html', {
        'form': form
    })

def registrar_tipo_equipo(request):
    if request.method == 'POST':
        form = Tipo_equipoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado_tipo_equipos')
    else:
        form = Tipo_equipoForm()

    return render(request, 'inventario/registro/registrar_tipo_equipo.html', {
        'form': form
    })

def registrar_procesador(request):
    if request.method == 'POST':
        form = ProcesadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado_procesadores')
    else:
        form = ProcesadorForm()

    return render(request, 'inventario/registro/registrar_procesador.html', {
        'form': form
    })


def registrar_sistema_operativo(request):
    if request.method == 'POST':
        form = SoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado_sistemas_operativos')
    else:
        form = SoForm()
    return render(request, 'inventario/registro/registrar_so.html', {'form': form})


def registrar_estado_equipo(request):
    if request.method == 'POST':
        form = Estado_equipoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado_estados')
    else:
        form = Estado_equipoForm()

    return render(request, 'inventario/registro/registrar_estado.html', {
        'form': form
    })



# Adicionales 
def obtener_marca(request):
    modelo_id = request.GET.get('modelo_id')

    if not modelo_id:
        return JsonResponse({'marca': ''})

    try:
        modelo = Modelo_equipo.objects.get(id=modelo_id)
        marca_nombre = modelo.marca.marca  # Asegúrate que modelo.marca es ForeignKey a Modelo_marca
        return JsonResponse({'marca': marca_nombre})
    except Modelo_equipo.DoesNotExist:
        return JsonResponse({'marca': ''})
