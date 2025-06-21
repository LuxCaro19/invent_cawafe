from django.urls import path
from ventas import views

urlpatterns = [
    path('lista_equipos/', views.listado_equipos, name='listado_equipos_venta'),
    path('lista_equipos_rrhh/', views.listado_equipos_rrhh, name='listado_equipos_rrhh'),
    path('lista_equipos_por_entregar/', views.listado_equipos_por_entregar, name='listado_equipos_por_entregar'),
    path('detalle_equipo/<int:id>/', views.detalle_equipo, name='detalle_equipo_venta'),
    path('detalle_equipo_rrhh/<int:id>/', views.detalle_equipo_rrhh, name='detalle_equipo_rrhh'),
    path('detalle_equipo_por_entregar/<int:id>/', views.detalleequipo_por_entregar, name='detalleequipo_por_entregar'),
    path('comprar_equipo/<int:id>/', views.comprar_equipo, name='comprar_equipo'),
    path('rrhh/equipo/<int:equipo_id>/<str:accion>/', views.accion_rrhh_equipo, name='accion_rrhh_equipo'),
    path('entregar_equipo/<int:equipo_id>/', views.confirmar_entrega, name='confirmar_entrega'),

]
