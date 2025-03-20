from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.index),
    path('detalle_equipo/<int:id>', views.detalle_equipo,name='detalle_equipo'),
    path('test/', views.listado_equipos)

]
