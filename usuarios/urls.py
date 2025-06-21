from django.urls import path
from . import views


urlpatterns = [
    path('usuarios/', views.lista_usuarios, name='usuarios_lista'),
    path('usuarios/crear/', views.usuario_crear, name='usuario_crear'),
]
