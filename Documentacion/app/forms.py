"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import InstruccionEmbarque
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


class ClienteForm(models.Model): # <<-- Asegúrate que el nombre sea 'Cliente' con C mayúscula
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nombre



class InstruccionEmbarqueForm(forms.ModelForm):
    class Meta:
        model = InstruccionEmbarque
        fields = '__all__' # Utilizar '__all__' es la forma más sencilla para ModelForms.

        # Si quisieras especificar los campos, deberían ser los nuevos nombres del modelo:
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
        #     # 'fecha_creacion', # Estos campos se manejan automáticamente
        #     # 'ultima_actualizacion', # Estos campos se manejan automáticamente
         ]

        widgets = {
            'fecha_embarque_estimada': forms.DateInput(attrs={'type': 'date'}),
            'descripcion_mercancia': forms.Textarea(attrs={'rows': 4}),
            # Puedes seguir añadiendo más widgets si lo necesitas:
             'instrucciones_especiales': forms.Textarea(attrs={'rows': 3}),
        }
