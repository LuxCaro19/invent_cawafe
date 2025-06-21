from django.urls import path
from . import views


urlpatterns = [
    path('usuarios/', views.lista_usuarios, name='usuarios_lista'),
    path('crear/', views.usuario_crear, name='usuario_crear'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('editar/<int:usuario_id>/', views.usuario_editar, name='usuario_editar'),

]
