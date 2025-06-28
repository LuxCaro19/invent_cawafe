from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils.timezone import now
from mantenciones.models import Tipo_mantencion, Mantencion, Registro_mantencion
from inventario.models import Equipo
from usuarios.models import Usuario  # Ajusta según tu app

def equipos_sin_mantencion(request):
    equipos = Equipo.objects.filter(mantencion__isnull=True)

    if request.method == "POST":
        seleccionados = request.POST.getlist('equipos')
        tipo, _ = Tipo_mantencion.objects.get_or_create(nombre='Creación', defaults={'frecuencia_dias': 30})

        # Buscar o crear usuario del sistema
        responsable, _ = Usuario.objects.get_or_create(
            correo='sistema@mantenciones.cl',
            defaults={
                'nombre_completo': 'Sistema Mantenciones',
                'rut': '99999999-9',
                'is_active': False,
            }
        )

        for equipo_id in seleccionados:
            try:
                equipo = Equipo.objects.get(id=equipo_id)
                mant = Mantencion.objects.create(equipo=equipo, tipo=tipo)
                Registro_mantencion.objects.create(
                    mantencion=mant,
                    fecha=now(),
                    responsable=responsable,
                    observaciones='Mantención inicial agregada manualmente.',
                    ubicacion='Desconocida',
                    tipo='Inicial'
                )
            except Equipo.DoesNotExist:
                continue

        messages.success(request, f"{len(seleccionados)} mantenciones creadas exitosamente.")
        return redirect('lista_mantenciones')

    return render(request, 'mantenciones/equipos_sin_mantencion.html', {'equipos': equipos})
