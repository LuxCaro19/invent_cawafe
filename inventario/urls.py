from django.urls import path
from . import views, views_reportes


urlpatterns = [
    # Página de inicio
    path('', views.index),

    # URLS DE DETALLE
    path('detalle_equipo/<int:id>/', views.detalle_equipo, name='detalle_equipo'),
    path('detalle_modelo/<int:id>/', views.detalle_modelo_equipo, name='detalle_modelo_equipo'),
    path('detalle_marca/<int:id>/', views.detalle_marca_equipo, name='detalle_marca'),
    path('detalle_tipo/<int:id>/', views.detalle_tipo_equipo, name='detalle_tipo_equipo'),
    path('detalle_procesador/<int:id>/', views.detalle_procesador, name='detalle_procesador'),
    path('detalle_so/<int:id>/', views.detalle_sistema_operativo, name='detalle_so'),
    path('detalle_estado/<int:id>/', views.detalle_estado_equipo, name='detalle_estado'),

    # URLS DE REGISTRO
    path('registrar_equipo/', views.registrar_equipo, name='registrar_equipo'),
    path('registrar_modelo_equipo/', views.registrar_modelo_equipo, name='registrar_modelo_equipo'),
    path('registrar_marca/', views.registrar_marca_equipo, name='registrar_marca'),
    path('registrar_tipo_equipo/', views.registrar_tipo_equipo, name='registrar_tipo_equipo'),
    path('registrar_procesador/', views.registrar_procesador, name='registrar_procesador'),
    path('registrar_so/', views.registrar_sistema_operativo, name='registrar_so'),
    path('registrar_estado_equipo/', views.registrar_estado_equipo, name='registrar_estado'),

    # URLS DE LISTAS
    path('lista_equipos/', views.listado_equipos, name='listado_equipos'),
    path('lista_modelo_equipos/', views.listado_modelo_equipo, name='listado_modelo_equipos'),
    path('lista_marcas/', views.listado_marcas, name='listado_marcas'),
    path('lista_tipos_equipos/', views.listado_tipo_equipos, name='listado_tipo_equipos'),
    path('lista_procesadores/', views.listado_procesadores, name='listado_procesadores'),
    path('lista_sistemas_operativos/', views.listado_sistemas_operativos, name='listado_sistemas_operativos'),
    path('lista_estado_equipos/', views.listado_estado_equipos, name='listado_estados'),

    # URLS ADICIONALES
    path('obtener_marca/', views.obtener_marca, name='obtener_marca'),
    path('reportes/', views_reportes.vista_reportes, name='vista_reportes'),
    path('reportes/inventario/', views_reportes.reporte_inventario_general, name='reporte_inventario_general'),
    path('reportes/venta/', views_reportes.reporte_equipos_para_venta, name='reporte_equipos_para_venta'),
    path('reportes/antiguedad/', views_reportes.reporte_antiguedad_equipos, name='reporte_antiguedad_equipos'),

]
