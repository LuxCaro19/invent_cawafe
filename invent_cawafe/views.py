
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def bienvenido(request):
    return render(request, 'bienvenido.html')


def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        password = request.POST.get('password')

        usuario = authenticate(request, correo=correo, password=password)

        if usuario  is not None:
            login(request, usuario)
            # Si el usuario es staff (admin), redirige a menú admin
            if usuario.is_staff:
                return redirect('menu_admin')
            else:
                return redirect('listado_equipos_venta')  # ejemplo de vista de empleado
        else:
            messages.error(request, 'Credenciales inválidas. Intente de nuevo.')

    return render(request, 'login.html')

def menu_admin(request):
    return render(request, 'menu_admin.html')