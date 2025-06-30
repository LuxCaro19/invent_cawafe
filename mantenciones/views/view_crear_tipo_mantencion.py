import json
from django.shortcuts import render, redirect
from mantenciones.forms import TipoMantencionForm, TareaTipoMantencionForm
from mantenciones.models import Tipo_mantencion, Tarea_tipo_mantencion
from inventario.models import Modelo_tipo, Sistema_operativo

def crear_tipo_mantencion(request):
    if request.method == 'POST':
        form = TipoMantencionForm(request.POST)
        tareas_json = request.POST.get('tareas_json', '[]')
        tareas = json.loads(tareas_json)

        if form.is_valid():
            if not tareas:
                form.add_error(None, "Debes agregar al menos una tarea.")
            else:
                tipo = form.save()
                for desc in tareas:
                    Tarea_tipo_mantencion.objects.create(tipo=tipo, descripcion=desc)
                return redirect('lista_tipos_mantencion')
    else:
        form = TipoMantencionForm()

    return render(request, 'mantenciones/crear_tipo_mantencion.html', {
        'form': form,
        'tipos_equipo_existentes': Modelo_tipo.objects.exists(),
        'sistemas_operativos_existentes': Sistema_operativo.objects.exists(),
    })

def crear_tarea(request):
    if request.method == 'POST':
        form = TareaTipoMantencionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('editar_tipo_mantencion', tipo_id=form.cleaned_data['tipo'].id)
    else:
        form = TareaTipoMantencionForm()

    return render(request, 'mantenciones/crear_tarea.html', {'form': form})
