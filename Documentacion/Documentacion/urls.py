"""
Definition of urls for Documentacion.
"""

from datetime import datetime
from django.urls import path # type: ignore
from django.contrib import admin # type: ignore
from django.contrib.auth.views import LoginView, LogoutView # type: ignore
from app import forms, views
from django.http import HttpResponseRedirect
from django.urls import reverse

def custom_logout(request):
    if request.method == 'GET':
        from django.contrib.auth import logout
        logout(request)
        return HttpResponseRedirect(reverse('login'))

urlpatterns = [
    path('', LoginView.as_view(
        template_name='app/login.html',
        next_page='home',
        extra_context={
            'title': 'Iniciar Sesión',
            'year': datetime.now().year,
        }
    ), name='login'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('logout/', custom_logout, name='logout'),
    path('admin/', admin.site.urls),

    path('crear_instruccion_embarque', views.crear_instruccion_embarque, name='crear_instruccion'),
    path('confirmacion_instruccion', views.confirmacion_instruccion, name='confirmacion_instruccion'),
    path('crear_reserva/', views.crear_reserva, name='crear_reserva'),
    path('mis_reservas/', views.mis_reservas, name='mis_reservas'),
    path('editar_reserva/<int:reserva_id>/', views.editar_reserva, name='editar_reserva'),
    path('eliminar_reserva/<int:reserva_id>/', views.eliminar_reserva, name='eliminar_reserva'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('servicios_adicionales/', views.servicios_adicionales, name='servicios_adicionales'),
    path('mapa/', views.mapa, name='mapa'),
    path('historial_reservas/', views.historial_reservas, name='historial_reservas'),
    path('autocomplete_puertos/', views.autocomplete_puertos_local, name='autocomplete_puertos'),
]