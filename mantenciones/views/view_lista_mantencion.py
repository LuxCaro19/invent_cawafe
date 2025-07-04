from django.shortcuts import render
from mantenciones.models import Mantencion
from datetime import date
from django.db import ProgrammingError

def lista_mantenciones(request):
    buscar = request.GET.get('buscar', '').strip()
    campo = request.GET.get('campo', '')
    agrupar = request.GET.get('agrupar', '')
    hoy = date.today()

    try:
        mantenciones = Mantencion.objects.select_related(
            'equipo__modelo__tipo',
            'tipo',
            'equipo__usuario_asignado__ubicacion'
        )

        # Filtro de texto
        if buscar:
            if campo == 'equipo':
                mantenciones = mantenciones.filter(equipo__etiqueta__icontains=buscar)
            elif campo == 'tipo_equipo':
                mantenciones = mantenciones.filter(equipo__modelo__tipo__tipo__icontains=buscar)
            elif campo == 'tipo':
                mantenciones = mantenciones.filter(tipo__nombre__icontains=buscar)
            elif campo == 'vigencia':
                if buscar.lower() == 'vigente':
                    mantenciones = mantenciones.filter(fecha_proxima__gte=hoy)
                elif buscar.lower() == 'atrasado':
                    mantenciones = mantenciones.filter(fecha_proxima__lt=hoy)

        # Anotamos última fecha y vigencia en cada mantención
        for m in mantenciones:
            m.ultima_fecha_valor = m.ultima_fecha()
            if m.fecha_proxima:
                m.vigencia = 'Vigente' if m.fecha_proxima >= hoy else 'Atrasado'
            else:
                m.vigencia = 'Sin datos'

        # Agrupar si corresponde
        grupos = {}
        if agrupar:
            for m in mantenciones:
                if agrupar == 'tipo':
                    clave = m.tipo.nombre if m.tipo else 'Sin tipo'
                elif agrupar == 'tipo_equipo':
                    clave = m.equipo.modelo.tipo.tipo if m.equipo and m.equipo.modelo and m.equipo.modelo.tipo else 'Sin tipo'
                elif agrupar == 'vigencia':
                    clave = m.vigencia
                elif agrupar == 'ubicacion':
                    clave = m.equipo.usuario_asignado.ubicacion.nombre if getattr(m.equipo.usuario_asignado, 'ubicacion', None) else 'Sin ubicación'
                else:
                    clave = 'Otros'
                grupos.setdefault(clave, []).append(m)
        else:
            grupos[''] = list(mantenciones)

    except ProgrammingError:
        grupos = {}

    return render(request, 'mantenciones/lista_mantenciones.html', {

        'grupos': grupos,
        'filtro_busqueda': buscar,
        'campo': campo,
        'agrupar': agrupar,
        'today': hoy,
    })
