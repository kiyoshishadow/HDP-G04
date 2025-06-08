# Documentacion/admin.py

from django.contrib import admin
from .models import InstruccionEmbarque, Cliente

# Registra el modelo Cliente en el admin para que puedas crear clientes
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono')
    search_fields = ('nombre', 'email')

@admin.register(InstruccionEmbarque)
class InstruccionEmbarqueAdmin(admin.ModelAdmin):
    list_display = (
        'get_shipper_nombre',
        'get_consignee_nombre',
        'puerto_carga',
        'puerto_descarga',
        'fecha_embarque_estimada',
        'tipo_servicio'
    )
    search_fields = (
        'shipper__nombre',
        'consignee__nombre',
        'descripcion_mercancia',
        'numero_contenedor'
    )
    # ¡Aqui es donde debes asegurarte de que list_filter este en una nueva línea!
    list_filter = (
        'fecha_creacion',
        'puerto_carga',           # Corregido de 'puerto_origen'
        'puerto_descarga',        # Corregido de 'puerto_destino'
        'tipo_servicio'
    )

    @admin.display(description='Shipper')
    def get_shipper_nombre(self, obj):
        return obj.shipper.nombre if obj.shipper else '-'

    @admin.display(description='Consignee')
    def get_consignee_nombre(self, obj):
        # Esta línea DEBE terminar aquí, antes de que comience list_filter
        return obj.consignee.nombre if obj.consignee else '-'
    # Aquí es donde va el salto de línea.
    # list_filter debe estar alineado con search_fields y list_display