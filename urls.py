"""
URL configuration for invent_cawafe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import bienvenido, login_view,menu_admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', bienvenido, name='bienvenido'),  # Página raíz
    path('login/', login_view, name='login'),
    path('admin/', admin.site.urls),
    path('inventario/', include('inventario.urls')),
    path('ventas/', include('ventas.urls')),
    path('menu_admin/', menu_admin, name='menu_admin'),
    path('usuarios/', include('usuarios.urls')),
    path('parametro/', include('parametro.urls')),
    path('asociacion/', include('asociacion.urls')),
    path('mantenciones/', include('mantenciones.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
