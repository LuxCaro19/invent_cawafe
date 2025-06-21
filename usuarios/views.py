from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from .models import Usuario 

def lista_usuarios(request):
    query = request.GET.get('q')

    if query:
        usuarios = Usuario.objects.filter(
            nombre_completo__icontains=query
        )
    else:
        usuarios = Usuario.objects.all()

    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})


def usuario_crear(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        rut = request.POST['rut']
        obra = request.POST['obra']
        sala = request.POST['sala']
        cargo = request.POST['cargo'] 
        rol = request.POST['rol']
        password = request.POST['password'] 

        Usuario.objects.create_user(
        correo=correo,
        nombre_completo=nombre,
        rut=rut,
        obra=obra,
        sala_venta=sala,
        cargo=cargo,
        password=password,
        is_staff=(rol == 'admin')
        )
        return redirect('usuarios_lista')  # Redirige al listado al guardar

    return render(request, 'usuarios/crear_usuario.html')

def usuario_editar(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        usuario.nombre_completo = request.POST['nombre']
        usuario.correo = request.POST['correo']
        usuario.rut = request.POST['rut']
        usuario.obra = request.POST['obra']
        usuario.sala_venta = request.POST['sala']
        usuario.cargo = request.POST['cargo']
        usuario.is_staff = (request.POST['rol'] == 'admin')
        usuario.is_active = 'activo' in request.POST

        nueva_password = request.POST['password']
        if nueva_password:
            usuario.password = make_password(nueva_password)

        usuario.save()
        return redirect('usuarios_lista')

    return render(request, 'usuarios/editar_usuario.html', {'usuario': usuario})

def cerrar_sesion(request):
    logout(request)
    return redirect('login')