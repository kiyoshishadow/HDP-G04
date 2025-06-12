"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import InstruccionEmbarque, ReservaCarga, Documento
from django.db import models
from django.contrib.auth.models import User
from .models import PerfilUsuario
from django.forms import ModelForm
from django.forms.widgets import DateInput, CheckboxSelectMultiple
from django.core.exceptions import ValidationError
from django.utils.timezone import now

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



class InstruccionEmbarqueForm(ModelForm):
    class Meta:
        model = InstruccionEmbarque
        fields = ['reserva', 'numero_booking', 'numero_contenedor', 'exportador', 'consignatario', 'notificar_a', 'puerto_embarque', 'puerto_destino', 'descripcion_carga', 'instrucciones_especiales', 'estado']
        widgets = {
            'exportador': forms.Textarea(attrs={'rows': 3}),
            'consignatario': forms.Textarea(attrs={'rows': 3}),
            'notificar_a': forms.Textarea(attrs={'rows': 3}),
            'descripcion_carga': forms.Textarea(attrs={'rows': 3}),
            'instrucciones_especiales': forms.Textarea(attrs={'rows': 3}),
        }




class ReservaCargaForm(forms.ModelForm):
    class Meta:
        model = ReservaCarga
        exclude = ['usuario', 'fecha_creacion_reserva', 'ultima_actualizacion_reserva', 'estado_reserva']
        widgets = {
            'fecha_embarque': DateInput(attrs={'type': 'date'}),
            'fecha_limite_llegada': DateInput(attrs={'type': 'date'}),
        }

class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cd['password2']

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        exclude = ['user']

class DocumentoForm(forms.ModelForm):
    """Formulario para la gestión de documentos de carga."""
    class Meta:
        model = Documento
        fields = [
            'tipo', 'puerto_objeto', 'archivo', 'numero_referencia', 
            'fecha_emision', 'fecha_vencimiento', 'es_obligatorio', 'es_original', 
            'observaciones'
        ]
        widgets = {
            'fecha_emision': DateInput(attrs={'type': 'date'}),
            'fecha_vencimiento': DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Añada cualquier observación relevante sobre el documento'}),
        }

    def __init__(self, *args, **kwargs):
        puertos_ruta = kwargs.pop('puertos_ruta', None)
        super(DocumentoForm, self).__init__(*args, **kwargs)
        from .models import Puerto
        if puertos_ruta:
            self.fields['puerto_objeto'].queryset = Puerto.objects.filter(nombre__in=puertos_ruta)
        self.fields['puerto_objeto'].required = False
        self.fields['puerto_objeto'].label = "Seleccionar Puerto (opcional)"
        self.fields['numero_referencia'].required = False
        self.fields['fecha_emision'].required = False
        self.fields['fecha_vencimiento'].required = False
        self.fields['observaciones'].required = False
        self.fields['es_obligatorio'].help_text = "Marque si este documento es obligatorio para el desembarco"
        self.fields['es_original'].help_text = "Marque si este documento es el original (no una copia)"


