from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from .models import Usuario 
from parametro.models import Ubicacion

def lista_usuarios(request):
    buscar = request.GET.get('buscar', '')
    agrupar = request.GET.get('agrupar', '')

    usuarios = Usuario.objects.all()

    if buscar:
        usuarios = usuarios.filter(
            Q(nombre_completo__icontains=buscar) |
            Q(correo__icontains=buscar) |
            Q(rut__icontains=buscar)
        )

    grupos = {}

    if agrupar == 'ubicacion':
        for usuario in usuarios:
            clave = usuario.ubicacion.nombre if usuario.ubicacion else "Sin ubicación"
            grupos.setdefault(clave, []).append(usuario)
    elif agrupar == 'rol':
        clave = lambda u: "Administrador" if u.is_staff else "Empleado"
        for usuario in usuarios:
            grupos.setdefault(clave(usuario), []).append(usuario)
    else:
        grupos['Todos'] = list(usuarios)

    return render(request, 'usuarios/lista_usuarios.html', {
        'grupos': grupos,
        'filtro_busqueda': buscar,
        'agrupar': agrupar,
    })


def usuario_crear(request):
    ubicaciones = Ubicacion.objects.all()

    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        rut = request.POST['rut']
        ubicacion_id = request.POST['ubicacion']
        cargo = request.POST['cargo']
        rol = request.POST['rol']
        password = request.POST['password']

        errores = []
        if Usuario.objects.filter(correo=correo).exists():
            errores.append("El correo ya está registrado.")
        if Usuario.objects.filter(rut=rut).exists():
            errores.append("El RUT ya está registrado.")

        if errores:
            for error in errores:
                messages.error(request, error)
            return render(request, 'usuarios/crear_usuario.html', {
                'ubicaciones': ubicaciones,
                'nombre': nombre,
                'correo': correo,
                'rut': rut,
                'cargo': cargo,
                'rol': rol,
            })

        Usuario.objects.create_user(
            correo=correo,
            nombre_completo=nombre,
            rut=rut,
            ubicacion_id=ubicacion_id,
            cargo=cargo,
            password=password,
            is_staff=(rol == 'admin')
        )
        return redirect('usuarios_lista')

    return render(request, 'usuarios/crear_usuario.html', {
        'ubicaciones': ubicaciones
    })


def usuario_editar(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    ubicaciones = Ubicacion.objects.all()

    if request.method == 'POST':
        usuario.nombre_completo = request.POST['nombre']
        usuario.correo = request.POST['correo']
        usuario.rut = request.POST['rut']
        ubicacion_id = request.POST.get('ubicacion')
        rol = request.POST.get('rol')
        password = request.POST.get('password')
        usuario.is_active = 'activo' in request.POST
        usuario.is_staff = (rol == 'admin')

        if ubicacion_id:
            usuario.ubicacion_id = ubicacion_id

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
