from django.urls import path
from . import views

urlpatterns = [
    path('lista_mantenciones/', views.lista_mantenciones, name='lista_mantenciones'),
    path('mantencion/<int:pk>/', views.detalle_mantencion, name='detalle_mantencion'),
    path('mantencion/<int:pk>/editar/', views.editar_mantencion, name='editar_mantencion'),
    path('mantencion/<int:mantencion_id>/nuevo_registro/', views.nueva_mantencion_registro, name='nueva_mantencion'),
    path('mantencion/tipo-mantencion/nuevo/', views.crear_tipo_mantencion, name='crear_tipo_mantencion'),
    path('mantencion/tarea/nueva/', views.crear_tarea, name='crear_tarea'),
    path('mantencion/tipos/', views.lista_tipos_mantencion, name='lista_tipos_mantencion'),
    path('mantencion/tipo/<int:pk>/', views.detalle_tipo_mantencion, name='detalle_tipo_mantencion'),
    path('mantenciones/sin/', views.equipos_sin_mantencion, name='equipos_sin_mantencion'),
    path('eliminar/<int:mantencion_id>/', views.eliminar_mantencion, name='eliminar_mantencion'),
    path('mantencion/<int:pk>/cambiar/', views.cambiar_mantencion, name='cambiar_mantencion'),
    path('mantenciones/tipo/<int:id>/editar/', views.editar_tipo_mantencion, name='editar_tipo_mantencion'),
    path('mantenciones/tipo/<int:tipo_id>/agregar_tarea/', views.agregar_tarea_tipo_mantencion, name='agregar_tarea_tipo_mantencion'),
    path('mantenciones/tipo/<int:tipo_id>/tarea/<int:tarea_id>/eliminar/', views.eliminar_tarea_tipo_mantencion, name='eliminar_tarea_tipo_mantencion'),

]

