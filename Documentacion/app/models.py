"""
Definition of models.
"""

# Documentacion/models.py

from django.db import models # type: ignore # <<-- Asegrate de que esta lnea est aqu!
from django.contrib.auth.models import User # type: ignore
import pycountry # type: ignore
import phonenumbers # type: ignore

class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class InstruccionEmbarque(models.Model):
    # Informaci�n de las partes
    shipper = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='instrucciones_como_shipper', verbose_name="Remitente")
    consignee = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='instrucciones_como_consignee', verbose_name="Consignatario")
    notify_party = models.ForeignKey(Cliente, on_delete=models.SET_NULL, related_name='instrucciones_como_notify_party', null=True, blank=True, verbose_name="Parte a Notificar")

    # Informaci�n de la ruta
    puerto_carga = models.CharField(max_length=100, verbose_name="Puerto de Carga (POL)")
    puerto_descarga = models.CharField(max_length=100, verbose_name="Puerto de Descarga (POD)")
    fecha_embarque_estimada = models.DateField(verbose_name="Fecha de Embarque Estimada")

    # Informaci�n de la carga
    descripcion_mercancia = models.TextField(verbose_name="Descripcion de la Mercancia")
    cantidad_bultos = models.IntegerField(verbose_name="Cantidad de Bultos")
    peso_bruto_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Peso Bruto (KG)")
    volumen_cbm = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Volumen (CBM)")

    # Informaci�n del contenedor (opcional)
    numero_contenedor = models.CharField(max_length=15, blank=True, null=True, verbose_name="Numero de Contenedor")
    numero_sello = models.CharField(max_length=15, blank=True, null=True, verbose_name="Numero de Sello")
    tipo_servicio = models.CharField(max_length=50, choices=[('FCL', 'Full Container Load'), ('LCL', 'Less than Container Load')], verbose_name="Tipo de Servicio")

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Instruccion de Embarque"
        verbose_name_plural = "Instrucciones de Embarque"
        # Agregamos ordering para el orden predeterminado en el admin/consultas
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"IE #{self.id} - {self.shipper.nombre} a {self.consignee.nombre}"

class ReservaCarga(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas', null=True, blank=True)
    # Información del Solicitante
    nombre_empresa_solicitante = models.CharField("Nombre Empresa Solicitante / Contacto", max_length=255)
    id_cliente_fk = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cliente Asociado (Opcional)")
    id_cliente_texto = models.CharField("ID de Cliente (Texto ingresado)", max_length=100, blank=True, null=True)
    email_contacto = models.EmailField("Email de Contacto")
    telefono_contacto = models.CharField("Teléfono de Contacto", max_length=30)

    # Referencia de Cotización
    numero_cotizacion = models.CharField("Número de Cotización", max_length=100, blank=True, null=True)

    # Detalles de la Carga
    descripcion_mercancia = models.TextField("Descripción de la Mercancía")
    tipo_mercancia = models.CharField("Tipo de Mercancía", max_length=50, choices=[
        ('general', 'General'),
        ('peligrosa', 'Peligrosa IMO Class'),
        ('refrigerada', 'Refrigerada'),
        ('perecedera', 'Perecedera'),
        ('sobredimensionada', 'Sobredimensionada'),
        ('otros', 'Otros'),
    ], default='general')
    peso_bruto_total = models.DecimalField("Peso Bruto Total", max_digits=12, decimal_places=2)
    unidad_peso = models.CharField("Unidad de Peso", max_length=3, choices=[
        ('KG', 'KG'),
        ('TON', 'Toneladas'),
        ('LBS', 'Libras'),
    ], default='KG')
    volumen_total = models.DecimalField("Volumen Total (CBM)", max_digits=10, decimal_places=2, blank=True, null=True)
    numero_bultos = models.IntegerField("Número de Bultos/Paquetes")
    codigo_hs = models.CharField("Código HS", max_length=100, blank=True, null=True)

    # Detalles del Contenedor
    tipo_contenedor = models.CharField("Tipo de Contenedor", max_length=50, choices=[
        ('20GP', "20' de uso general"),
        ('40GP', "40' de uso general"),
        ('40HC', "Cubo alto de uso general de 40 pies"),
        ('refrigerado', "Contenedor frigorífico"),
    ])
    cantidad_contenedores = models.IntegerField("Cantidad de Contenedores")
    condiciones_especiales_contenedor = models.CharField("Condiciones Especiales del Contenedor", max_length=255, blank=True, null=True)

    # Ruta y Fechas
    puerto_origen = models.CharField("Puerto de Origen (POL)", max_length=100)
    puerto_destino = models.CharField("Puerto de Destino (POD)", max_length=100)
    puerto_transbordo = models.CharField("Puerto de Transbordo", max_length=100, blank=True, null=True)
    fecha_embarque = models.DateField("Fecha Estimada de Embarque (ETD)")
    fecha_limite_llegada = models.DateField("Fecha Límite de Llegada", blank=True, null=True)
    viaje_buque = models.CharField("Selección de Viaje/Buque Específico", max_length=100, blank=True, null=True)

    # Partes Involucradas
    shipper_nombre = models.CharField("Shipper: Nombre Completo / Razón Social", max_length=255)
    shipper_direccion = models.TextField("Shipper: Dirección Completa")
    shipper_telefono = models.CharField("Shipper: Teléfono de Contacto", max_length=30)
    shipper_email = models.EmailField("Shipper: Email de Contacto")

    consignee_nombre = models.CharField("Consignee: Nombre Completo / Razón Social", max_length=255)
    consignee_direccion = models.TextField("Consignee: Dirección Completa")
    consignee_telefono = models.CharField("Consignee: Teléfono de Contacto", max_length=30)
    consignee_email = models.EmailField("Consignee: Email de Contacto")

    notify_nombre = models.CharField("Notify Party: Nombre Completo / Razón Social", max_length=255, blank=True, null=True)
    notify_direccion = models.TextField("Notify Party: Dirección Completa", blank=True, null=True)
    notify_telefono = models.CharField("Notify Party: Teléfono de Contacto", max_length=30, blank=True, null=True)
    notify_email = models.EmailField("Notify Party: Email de Contacto", blank=True, null=True)

    # Servicios Adicionales
    seguro_carga = models.BooleanField("Seguro de Carga", default=False)
    despacho_origen = models.BooleanField("Despacho Aduanal en Origen", default=False)
    despacho_destino = models.BooleanField("Despacho Aduanal en Destino", default=False)
    transporte_origen = models.BooleanField("Transporte Terrestre en Origen (Pre-carriage)", default=False)
    transporte_destino = models.BooleanField("Transporte Terrestre en Destino (On-carriage)", default=False)
    otros_servicios = models.CharField("Otros Servicios (Especificar)", max_length=255, blank=True, null=True)

    # Instrucciones Especiales / Comentarios
    instrucciones_especiales = models.TextField("Instrucciones Especiales / Comentarios", blank=True, null=True)

    # Carga Refrigerada
    temperatura_requerida = models.DecimalField("Temperatura Requerida", max_digits=5, decimal_places=1, blank=True, null=True)
    unidad_temperatura = models.CharField("Unidad de Temperatura", max_length=1, choices=[
        ('C', '°C'),
        ('F', '°F'),
    ], blank=True, null=True)
    ventilacion_requerida = models.BooleanField("Ventilación Requerida", default=False)

    # Carga Peligrosa
    numero_un = models.CharField("Número UN", max_length=50, blank=True, null=True)
    imo_class = models.CharField("IMO Class", max_length=50, blank=True, null=True)
    packing_group = models.CharField("Packing Group", max_length=50, blank=True, null=True)

    # Notas sobre Documentación
    notas_documentacion = models.TextField("Notas sobre Documentación", blank=True, null=True)

    # Auditoría
    fecha_creacion_reserva = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación de Reserva")
    ultima_actualizacion_reserva = models.DateTimeField(auto_now=True, verbose_name="Última Actualización de Reserva")

    # Estado de la Reserva
    estado_reserva = models.CharField("Estado de la Reserva", max_length=20, choices=[
        ('solicitada', 'Solicitada'),
        ('confirmada', 'Confirmada'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ], default='solicitada')

    class Meta:
        verbose_name = "Reserva de Carga"
        verbose_name_plural = "Reservas de Carga"
        ordering = ['-fecha_creacion_reserva']

    def __str__(self):
        return f"Reserva #{self.pk} - {self.nombre_empresa_solicitante} - {self.puerto_origen} a {self.puerto_destino}"

def get_all_country_code_choices():
    countries = list(pycountry.countries)
    choices = set()
    for country in countries:
        try:
            code = phonenumbers.country_code_for_region(country.alpha_2)
            if code:
                choices.add((f"+{code}", f"+{code} {country.name}"))
        except Exception:
            continue
    return sorted(list(choices), key=lambda x: x[1])

COUNTRY_CODE_CHOICES = get_all_country_code_choices()

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country_code = models.CharField("Código del país", max_length=10, choices=COUNTRY_CODE_CHOICES)
    phone = models.CharField("Número de teléfono", max_length=30)
    company = models.CharField("Nombre de empresa", max_length=255)
    tax_id = models.CharField("Impuesto de Sociedades / Registro / Número de IVA", max_length=100)
    address = models.CharField("Dirección de la calle / Número", max_length=255)
    city = models.CharField("Ciudad", max_length=100)
    postal_code = models.CharField("Código postal", max_length=20)

    def __str__(self):
        return f"Perfil de {self.user.username}"