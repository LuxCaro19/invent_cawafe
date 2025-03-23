from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.index),
    path('detalle_equipo/<int:id>/', views.detalle_equipo,name='detalle_equipo'),
    path('lista_equipos/', views.listado_equipos, name='listado_equipos'),
    path('registrar_equipo/', views.registrar_equipo, name='registrar_equipo')
]
