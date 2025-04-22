from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.index),
    #URLS DE DETALLE
    path('detalle_equipo/<int:id>/', views.detalle_equipo,name='detalle_equipo'),
    path('detalle_modelo/<int:id>/', views.detalle_modelo_equipo,name='detalle_modelo_equipo'),
    path('detalle_marca/<int:id>/', views.detalle_marca_equipo,name='detalle_marca'),
    path('detalle_tipo/<int:id>/', views.detalle_tipo_equipo,name='detalle_tipo_equipo'),
    
    #URLS DE REGISTRO
    path('registrar_equipo/', views.registrar_equipo, name='registrar_equipo'),
    path('registrar_modelo_equipo/', views.registrar_modelo_equipo, name='registrar_modelo_equipo'),
    path('registrar_marca/', views.registrar_marca_equipo, name='registrar_marca'),
    path('registrar_tipo_equipo/', views.registrar_tipo_equipo, name='registrar_tipo_equipo'),

    #URLS DE LISTAS
    path('lista_modelo_equipos/', views.listado_modelo_equipo, name='listado_modelo_equipos'),
    path('lista_equipos/', views.listado_equipos, name='listado_equipos'),
    path('lista_marcas/', views.listado_marcas, name='listado_marcas'),
    path('lista_tipos_equipos/', views.listado_tipo_equipos, name='listado_tipo_equipos')
]
