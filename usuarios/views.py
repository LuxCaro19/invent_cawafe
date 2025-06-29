from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from .models import Usuario 
from parametro.models import Ubicacion

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

    ubicaciones = Ubicacion.objects.all() 

    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        rut = request.POST['rut']
        ubicacion_id = request.POST['ubicacion']  # <- recibe ID, lo asignaremos con _id
        cargo = request.POST['cargo'] 
        rol = request.POST['rol']
        password = request.POST['password'] 

        Usuario.objects.create_user(
        correo=correo,
        nombre_completo=nombre,
        rut=rut,
        ubicacion_id=ubicacion_id,  # <- Asignación correcta con _id
        cargo=cargo,
        password=password,
        is_staff=(rol == 'admin')
        )
        return redirect('usuarios_lista')  # Redirige al listado al guardar

    return render(request, 'usuarios/crear_usuario.html', {
        'ubicaciones': ubicaciones
    })

def usuario_editar(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    ubicaciones = Ubicacion.objects.all()

    if request.method == 'POST':
        usuario.nombre_completo = request.POST['nombre']
        usuario.correo = request.POST['correo']
        usuario.rut = request.POST['rut']
        ubicacion_id = request.POST.get('ubicacion')  # <-- capturamos ubicación
        rol = request.POST.get('rol')
        password = request.POST.get('password')
        usuario.is_active = 'activo' in request.POST
        usuario.is_staff = (rol == 'admin')

        if ubicacion_id:
            usuario.ubicacion_id = ubicacion_id  # <-- guardamos ubicación

        if password:
            usuario.set_password(password)

        usuario.save()
        return redirect('usuarios_lista')

    return render(request, 'usuarios/editar_usuario.html', {
        'usuario': usuario,
        'ubicaciones': ubicaciones,
    })

def cerrar_sesion(request):
    logout(request)
    return redirect('login')