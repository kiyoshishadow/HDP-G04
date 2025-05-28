"""
Definition of urls for Documentacion.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),    path('login/', 
         LoginView.as_view(
             template_name='app/login.html',
             next_page='home',
             extra_context={
                 'title': 'Iniciar Sesión',
                 'year': datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),

    path('crear_instruccion_embarque', views.crear_instruccion_embarque, name='crear_instruccion'),
    path('confirmacion_instruccion', views.confirmacion_instruccion, name='confirmacion_instruccion'),
    path('crear_reserva/', views.crear_reserva, name='crear_reserva'),
    path('mis_reservas/', views.mis_reservas, name='mis_reservas'),
    path('editar_reserva/<int:reserva_id>/', views.editar_reserva, name='editar_reserva'),
    path('eliminar_reserva/<int:reserva_id>/', views.eliminar_reserva, name='eliminar_reserva'),
]