"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import InstruccionEmbarque, ReservaCarga
from django.db import models

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
        fields = '__all__' # Utilizar '__all__' es la forma m�s sencilla para ModelForms.

        # Si quisieras especificar los campos, deber�an ser los nuevos nombres del modelo:
        fields = [
             'shipper',
             'consignee',
             'notify_party',
             'puerto_carga',
             'puerto_descarga',
             'fecha_embarque_estimada',
             'descripcion_mercancia',
             'cantidad_bultos',
             'peso_bruto_kg',
             'volumen_cbm',
             'numero_contenedor',
             'numero_sello',
             'tipo_servicio',
        #     # 'fecha_creacion', # Estos campos se manejan autom�ticamente
        #     # 'ultima_actualizacion', # Estos campos se manejan autom�ticamente
         ]

        widgets = {
            'fecha_embarque_estimada': forms.DateInput(attrs={'type': 'date'}),
            'descripcion_mercancia': forms.Textarea(attrs={'rows': 4}),
            # Puedes seguir a�adiendo m�s widgets si lo necesitas:
             'instrucciones_especiales': forms.Textarea(attrs={'rows': 3}),
        }


class ReservaCargaForm(forms.ModelForm):
    class Meta:
        model = ReservaCarga
        fields = '__all__'
        exclude = ['estado_reserva'] # Excluir el campo estado_reserva
        widgets = {
            'fecha_embarque': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_limite_llegada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion_mercancia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'instrucciones_especiales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notas_documentacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
