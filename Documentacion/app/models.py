"""
Definition of models.
"""

# Documentacion/models.py

from django.db import models # <<-- ¡Asegúrate de que esta línea esté aquí!

class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class InstruccionEmbarque(models.Model):
    # Información de las partes
    shipper = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='instrucciones_como_shipper', verbose_name="Remitente")
    consignee = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='instrucciones_como_consignee', verbose_name="Consignatario")
    notify_party = models.ForeignKey(Cliente, on_delete=models.SET_NULL, related_name='instrucciones_como_notify_party', null=True, blank=True, verbose_name="Parte a Notificar")

    # Información de la ruta
    puerto_carga = models.CharField(max_length=100, verbose_name="Puerto de Carga (POL)")
    puerto_descarga = models.CharField(max_length=100, verbose_name="Puerto de Descarga (POD)")
    fecha_embarque_estimada = models.DateField(verbose_name="Fecha de Embarque Estimada")

    # Información de la carga
    descripcion_mercancia = models.TextField(verbose_name="Descripcion de la Mercancia")
    cantidad_bultos = models.IntegerField(verbose_name="Cantidad de Bultos")
    peso_bruto_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Peso Bruto (KG)")
    volumen_cbm = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Volumen (CBM)")

    # Información del contenedor (opcional)
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