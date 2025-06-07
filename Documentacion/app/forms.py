"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import InstruccionEmbarque, ReservaCarga
from django.db import models
from django.contrib.auth.models import User
from .models import PerfilUsuario

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class ClienteForm(models.Model): # <<-- Aseg�rate que el nombre sea 'Cliente' con C may�scula
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nombre



class InstruccionEmbarqueForm(forms.ModelForm):
    class Meta:
        model = InstruccionEmbarque
        fields = [
            'numero_booking',
            'numero_contenedor',
            'exportador',
            'consignatario',
            'notificar_a',
            'puerto_embarque',
            'puerto_destino',
            'descripcion_carga',
            'instrucciones_especiales',
        ]
        widgets = {
            'exportador': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'consignatario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notificar_a': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'descripcion_carga': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'instrucciones_especiales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'numero_booking': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: HLBU1234567'}),
            'numero_contenedor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: HLBU1234567'}),
            'puerto_embarque': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Guayaquil, Ecuador'}),
            'puerto_destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Callao, Perú'}),
        }
        labels = {
            'numero_booking': 'Número de Booking *',
            'numero_contenedor': 'Número de Contenedor *',
            'exportador': 'Exportador *',
            'consignatario': 'Consignatario *',
            'notificar_a': 'Notificar a',
            'puerto_embarque': 'Puerto de Embarque *',
            'puerto_destino': 'Puerto de Destino *',
            'descripcion_carga': 'Descripción de la Carga *',
            'instrucciones_especiales': 'Instrucciones Especiales',
        }




class ReservaCargaForm(forms.ModelForm):
    class Meta:
        model = ReservaCarga
        fields = [
            'nombre_empresa_solicitante',
            'id_cliente_texto',
            'email_contacto',
            'telefono_contacto',
            'numero_cotizacion',
            'descripcion_mercancia',
            'tipo_mercancia',
            'peso_bruto_total',
            'unidad_peso',
            'volumen_total',
            'numero_bultos',
            'codigo_hs',
            'tipo_contenedor',
            'cantidad_contenedores',
            'condiciones_especiales_contenedor',
            'puerto_origen',
            'puerto_destino',
            'puerto_transbordo',
            'fecha_embarque',
            'fecha_limite_llegada',
            'viaje_buque',
            'shipper_nombre',
            'shipper_direccion',
            'shipper_telefono',
            'shipper_email',
            'consignee_nombre',
            'consignee_direccion',
            'consignee_telefono',
            'consignee_email',
            'notify_nombre',
            'notify_direccion',
            'notify_telefono',
            'notify_email',
            'seguro_carga',
            'despacho_origen',
            'despacho_destino',
            'transporte_origen',
            'transporte_destino',
            'otros_servicios',
            'instrucciones_especiales',
            'temperatura_requerida',
            'unidad_temperatura',
            'ventilacion_requerida',
            'numero_un',
            'imo_class',
            'packing_group',
            'notas_documentacion',
        ]
        exclude = ['estado_reserva'] # Excluir el campo estado_reserva
        widgets = {
            'fecha_embarque': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_limite_llegada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion_mercancia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'instrucciones_especiales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notas_documentacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'id_cliente_texto': 'ID de Cliente (Opcional)',
        }

class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        return cleaned_data

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['country_code', 'phone', 'company', 'tax_id', 'address', 'city', 'postal_code', 'country']
        widgets = {
            'country_code': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'tax_id': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-select'}),
        }
