from django.shortcuts import render

def bienvenido(request):
    return render(request, 'bienvenido.html')

def login_view(request):
    return render(request, 'login.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Si el usuario es staff (admin), redirige a menú admin
            if user.is_staff:
                return redirect('menu_admin')
            else:
                return redirect('ventas:listado_equipos_venta')  # ejemplo de vista de empleado
        else:
            messages.error(request, 'Credenciales inválidas. Intente de nuevo.')

    return render(request, 'login.html')

def menu_admin(request):
    return render(request, 'menu_admin.html')