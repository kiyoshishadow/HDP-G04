"""
Definition of urls for Documentacion.
"""

from datetime import datetime
from django.urls import path # type: ignore
from django.contrib import admin # type: ignore
from django.contrib.auth.views import LoginView, LogoutView # type: ignore
from app import forms, views
from django.http import HttpResponseRedirect # type: ignore # type: ignore
from django.urls import reverse # type: ignore
from django.conf import settings
from django.conf.urls.static import static

def custom_logout(request):
    if request.method == 'GET':
        from django.contrib.auth import logout # type: ignore
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
    path('mis_embarques/', views.mis_embarques, name='mis_embarques'),
    path('instrucciones_embarque/', views.instrucciones_embarque, name='instrucciones_embarque'),
    path('aprobar_bl/', views.aprobar_bl, name='aprobar_bl'),
    path('documentos_embarque/', views.documentos_embarque, name='documentos_embarque'),
    path('editar_instruccion/<int:pk>/', views.editar_instruccion, name='editar_instruccion'),
    path('aprobar_instruccion/<int:pk>/', views.aprobar_instruccion, name='aprobar_instruccion'),
    path('descargar_bl/<int:pk>/', views.descargar_bl, name='descargar_bl'),
    path('detalle_embarque/<int:embarque_id>/', views.detalle_embarque, name='detalle_embarque'),
    path('validar_documento/<int:documento_id>/', views.validar_documento, name='validar_documento'),
    path('rechazar_documento/<int:documento_id>/', views.rechazar_documento, name='rechazar_documento'),
    path('documentos_pendientes/', views.documentos_pendientes, name='documentos_pendientes'),
    path('datos_reserva/', views.datos_reserva, name='datos_reserva'),
    path('eliminar_documento/<int:documento_id>/', views.eliminar_documento, name='eliminar_documento'),
    path('eliminar_instruccion/<int:embarque_id>/', views.eliminar_instruccion, name='eliminar_instruccion'),
    path('descargar_documentos_zip/<int:embarque_id>/', views.descargar_documentos_zip, name='descargar_documentos_zip'),
    path('mis_documentos_usuario/', views.mis_documentos_usuario, name='mis_documentos_usuario'),
    path('subir_documentos_usuario/', views.subir_documentos_usuario, name='subir_documentos_usuario'),
    path('aceptar_documentacion_usuario/', views.aceptar_documentacion_usuario, name='aceptar_documentacion_usuario'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)