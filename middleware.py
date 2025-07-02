from django.shortcuts import redirect
from django.urls import resolve
from django.contrib.auth.views import redirect_to_login

# Vistas permitidas para empleados
PERMITIDAS_PARA_EMPLEADO = ['listado_equipos_venta', 'detalle_equipo_venta', 'logout','comprar_equipo']

class EmpleadoRestriccionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            nombre_vista = resolve(request.path_info).url_name
        except:
            nombre_vista = None

        # Evitar bucle en login o cuando no hay vista resuelta
        if nombre_vista in ['login'] or nombre_vista is None:
            return self.get_response(request)

        if request.user.is_authenticated:
            if not request.user.is_staff:
                if nombre_vista not in PERMITIDAS_PARA_EMPLEADO:
                    return redirect('listado_equipos_venta')
        else:
            return redirect_to_login(request.get_full_path())

        return self.get_response(request)
