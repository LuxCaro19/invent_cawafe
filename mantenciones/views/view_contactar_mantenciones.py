from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from mantenciones.models import Mantencion
from usuarios.models import Usuario
from parametro.models import Ubicacion

from datetime import datetime

# Diccionario para traducir meses al español
MESES_ES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio",
    7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}

def formatear_fecha(fecha_str):
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        return f"{fecha.day} de {MESES_ES[fecha.month]} de {fecha.year}"
    except Exception:
        return fecha_str  # En caso de error, devuelve sin formato

def contactar_mantenciones(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario')
        ubicacion_id = request.POST.get('ubicacion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        if not usuario_id or not ubicacion_id or not fecha_inicio or not fecha_fin:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('contactar_mantenciones')

        usuario = Usuario.objects.get(id=usuario_id)
        ubicacion = Ubicacion.objects.get(id=ubicacion_id)

        # Obtener correos desde mantenciones para copia (CC)
        ids = request.GET.getlist('ids')
        mantenciones = Mantencion.objects.filter(id__in=ids).select_related('equipo__usuario_asignado')

        correos = set()
        for m in mantenciones:
            u = getattr(m.equipo, 'usuario_asignado', None)
            if u and u.correo and u.correo != usuario.correo:
                correos.add(u.correo)

        # Preparar contenido del correo
        contexto = {
            'usuario': usuario,
            'ubicacion': ubicacion.nombre,
            'fecha_inicio': formatear_fecha(fecha_inicio),
            'fecha_fin': formatear_fecha(fecha_fin),
            'remitente': request.user,
        }

        html_message = render_to_string('correos/mensaje_mantencion.html', contexto)
        plain_message = strip_tags(html_message)

        try:
            email = EmailMessage(
                subject='🔧 Mantención programada en equipos de TI',
                body=html_message,
                from_email='soporte.ti@galilea.cl',
                to=[usuario.correo],
                cc=list(correos),
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)
            messages.success(request, "📨 Correo enviado correctamente.")
        except Exception as e:
            messages.error(request, f"Error al enviar el correo: {e}")

        return redirect('lista_mantenciones')

    # Si GET: mostrar formulario
    ids = request.GET.getlist('ids')
    mantenciones = Mantencion.objects.filter(id__in=ids).select_related(
        'equipo__modelo__tipo',
        'equipo__usuario_asignado__ubicacion'
    )

    # Generar lista de correos únicos y usuario sugerido
    correos = set()
    conteo_usuarios = {}
    ubicacion_por_usuario = {}

    for m in mantenciones:
        usuario = getattr(m.equipo, 'usuario_asignado', None)
        if usuario:
            conteo_usuarios[usuario.id] = conteo_usuarios.get(usuario.id, 0) + 1
            ubicacion_por_usuario[usuario.id] = usuario.ubicacion
            if usuario.correo:
                correos.add(usuario.correo)

    ubicacion_seleccionada_id = request.GET.get("ubicacion") or None

    if not ubicacion_seleccionada_id:
        usuario_destacado_id = max(conteo_usuarios, key=conteo_usuarios.get) if conteo_usuarios else None
        ubicacion_seleccionada = ubicacion_por_usuario.get(usuario_destacado_id) if usuario_destacado_id else None
        ubicacion_seleccionada_id = ubicacion_seleccionada.id if ubicacion_seleccionada else None
    else:
        usuario_destacado_id = None

    return render(request, 'contactar_mantenciones.html', {
        'mantenciones': mantenciones,
        'correos': sorted(correos),
        'usuarios': Usuario.objects.all(),
        'usuario_destacado_id': usuario_destacado_id,
        'ubicaciones': Ubicacion.objects.all(),
        'ubicacion_seleccionada_id': int(ubicacion_seleccionada_id) if ubicacion_seleccionada_id else None,
    })
