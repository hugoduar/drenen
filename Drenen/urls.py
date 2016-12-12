"""Drenen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required


from app import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home , name='home'),
    url(r'^register$', views.register, name="register"),
    url(r'^faq$', views.faq, name="faq"),
    url(r'^contacto$', views.contacto, name="contacto"),
    url(r'^reporte$', views.reporte, name="reporte"),
    url(r'^aprobar_reporte$', views.aprobar_reporte, name="aprobar_reporte"),
    url(r'^entrada$', views.entrada, name="entrada"),
    url(r'^noticia/(?P<num>[0-9]+)$', views.noticia, name="noticia"),
    url(r'^modificar_entrada$', views.modificar_entrada, name="modificar_entrada"),
    url(r'^eliminar_entrada$', views.eliminar_entrada, name="eliminar_entrada"),
    url(r'^alumno$', login_required(views.home_alumno, login_url='/'), name="home_alumno"),
    url(r'^coordinador$', views.home_coordinador, name="home_alumno"),
    url(r'^administrador$', views.home_administrador, name="home_alumno"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^login$', views.login, name="login"),
    url(r'^enviar_alerta$', views.enviar_alerta, name="enviar_alerta"),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
