from django.urls import path
from . import views

urlpatterns = [
    path('lista_mantenciones/', views.lista_mantenciones, name='lista_mantenciones'),
    path('mantencion/<int:pk>/', views.detalle_mantencion, name='detalle_mantencion'),
    path('mantencion/<int:pk>/editar/', views.editar_mantencion, name='editar_mantencion'),
    path('mantencion/<int:mantencion_id>/nuevo_registro/', views.nueva_mantencion_registro, name='nueva_mantencion'),
]

