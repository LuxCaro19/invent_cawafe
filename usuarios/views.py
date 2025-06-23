from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from .models import Usuario 
from parametro.models import Obra, SalaVenta

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

    obras = Obra.objects.all()
    salas = SalaVenta.objects.all()

    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        rut = request.POST['rut']
        obra_id = request.POST['obra']  # <- recibe ID, lo asignaremos con _id
        sala_id = request.POST['sala']
        cargo = request.POST['cargo'] 
        rol = request.POST['rol']
        password = request.POST['password'] 

        Usuario.objects.create_user(
        correo=correo,
        nombre_completo=nombre,
        rut=rut,
        obra_id=obra_id,  # <- Asignación correcta con _id
        sala_venta_id=sala_id,
        cargo=cargo,
        password=password,
        is_staff=(rol == 'admin')
        )
        return redirect('usuarios_lista')  # Redirige al listado al guardar

    return render(request, 'usuarios/crear_usuario.html', {
        'obras': obras,
        'salas': salas
    })

def usuario_editar(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    obras = Obra.objects.all()
    salas = SalaVenta.objects.all()

    if request.method == 'POST':
        usuario.nombre_completo = request.POST['nombre']
        usuario.correo = request.POST['correo']
        usuario.rut = request.POST['rut']
        usuario.obra = Obra.objects.get(id=int(request.POST['obra']))
        usuario.sala_venta = SalaVenta.objects.get(id=int(request.POST['sala']))
        usuario.cargo = request.POST['cargo']
        usuario.is_staff = (request.POST['rol'] == 'admin')
        usuario.is_active = 'activo' in request.POST

        nueva_password = request.POST['password']
        if nueva_password:
            usuario.password = make_password(nueva_password)

        usuario.save()
        return redirect('usuarios_lista')

    return render(request, 'usuarios/editar_usuario.html', {
        'usuario': usuario,
        'obras': obras,
        'salas': salas
    })

def cerrar_sesion(request):
    logout(request)
    return redirect('login')