from django.urls import path
from . import views

urlpatterns = [
    path('', views.parametro_home, name='parametro_home'),
    path('obras/', views.obras_listar, name='obras_listar'),
    path('obras/crear/', views.obra_crear, name='obra_crear'),
    path('obras/editar/<int:obra_id>/', views.obra_editar, name='obra_editar'),
    path('obras/eliminar/<int:obra_id>/', views.obra_eliminar, name='obra_eliminar'),
    path('salas/', views.salas_listar, name='salas_listar'),
    path('salas/crear/', views.sala_crear, name='sala_crear'),
    path('salas/editar/<int:sala_id>/', views.sala_editar, name='sala_editar'),
    path('salas/eliminar/<int:sala_id>/', views.sala_eliminar, name='sala_eliminar'),
    path('ubicaciones/', views.ubicacion_admin, name='ubicacion_admin'),
    path('ubicaciones/nueva/', views.ubicacion_nueva, name='ubicacion_nueva'),
    path('ubicaciones/editar/<int:id>/', views.ubicacion_editar, name='ubicacion_editar'),
    path('ubicaciones/eliminar/<int:id>/', views.ubicacion_eliminar, name='ubicacion_eliminar'),

]
