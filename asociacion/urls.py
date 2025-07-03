# asociacion/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.vista_asociacion, name='vista_asociacion'),
    path('historial/<int:equipo_id>/', views.historial_equipo, name='historial_equipo'),
    path('lista/', views.vista_lista_asociaciones, name='lista_asociaciones'),
    path('autocomplete/equipos/', views.autocomplete_equipos, name='autocomplete_equipos'),
    path('autocomplete/usuarios/', views.autocomplete_usuarios, name='autocomplete_usuarios'),
    #path('ver/', views.ver_asociaciones, name='ver_asociaciones'),  # ← Asegúrate de tener esta línea
    path('buscar/', views.buscar_equipo_asociar, name='buscar_equipo_asociar'),

]
