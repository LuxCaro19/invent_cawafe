from django.shortcuts import render
from .models import Usuario 

def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

def usuario_crear(request):
    # Puedes redirigir temporalmente o mostrar un mensaje de "en construcción"
    return render(request, 'usuarios/crear_usuario.html')