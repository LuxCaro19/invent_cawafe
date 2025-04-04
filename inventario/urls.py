from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.index),
    #URLS DE DETALLE
    path('detalle_equipo/<int:id>/', views.detalle_equipo,name='detalle_equipo'),
    path('detalle_modelo/<int:id>/', views.detalle_modelo_equipo,name='detalle_modelo_equipo'),
    
    #URLS DE REGISTRO
    path('registrar_equipo/', views.registrar_equipo, name='registrar_equipo'),
    path('registrar_modelo_equipo/', views.registrar_modelo_equipo, name='registrar_modelo_equipo'),

    #URLS DE LISTAS
    path('lista_modelo_equipos/', views.listado_modelo_equipo, name='listado_modelo_equipos'),
    path('lista_equipos/', views.listado_equipos, name='listado_equipos')
]
