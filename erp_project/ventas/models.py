from django.db import models
from django.contrib.auth.models import User
from clientes.models import Cliente
from inventario.models import Producto
from usuarios.models import PerfilUsuario  # O usa User directamente

##falta mejorar aun

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    vendedor = models.ForeignKey(PerfilUsuario, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo_documento = models.CharField(
        max_length=20, 
        choices=[
            ('Boleta', 'Boleta'), 
            ('Factura', 'Factura'), 
            ('Nota de Crédito', 'Nota de Crédito'),
            ('Nota de Débito', 'Nota de Débito'),
            ('Devolución', 'Devolución'),
            ('Sin Documento', 'Sin Documento')
        ], 
        default='Boleta'
    )
    folio = models.CharField(max_length=30, blank=True)
    venta_original = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='notas_asociadas',
        help_text='Si esta venta es una nota de crédito/débito o devolución, referencia a la venta original'
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pdf = models.FileField(upload_to='ventas/pdfs/', blank=True, null=True)

    def tipo_afectacion(self):
        if self.tipo_documento == 'Nota de Crédito' or self.tipo_documento == 'Devolución':
            return 'Disminuye'
        elif self.tipo_documento == 'Nota de Débito':
            return 'Aumenta'
        else:
            return 'Directa'

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario


class FolioCounter(models.Model):
    """Mantiene el contador de folios por tipo de documento"""
    tipo_documento = models.CharField(
        max_length=20,
        choices=[
            ('Boleta', 'Boleta'), 
            ('Factura', 'Factura'), 
            ('Nota de Crédito', 'Nota de Crédito'),
            ('Nota de Débito', 'Nota de Débito'),
            ('Devolución', 'Devolución'),
            ('Sin Documento', 'Sin Documento')
        ],
        unique=True
    )
    contador = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.tipo_documento}: {self.contador}"
    
    class Meta:
        verbose_name_plural = "Folio Counters"
    
    @classmethod
    def obtener_proximo_folio(cls, tipo_documento):
        """Obtiene el próximo folio para un tipo de documento"""
        obj, created = cls.objects.get_or_create(tipo_documento=tipo_documento)
        if created:
            # Si se creó ahora, buscar el máximo folio existente en ventas
            max_venta = Venta.objects.filter(tipo_documento=tipo_documento).order_by('-folio').first()
            if max_venta and max_venta.folio:
                try:
                    # Intentar extraer número del folio (ej: "BOL-001" → 1)
                    numero = int(''.join(filter(str.isdigit, max_venta.folio)))
                    obj.contador = numero + 1
                    obj.save()
                except:
                    obj.contador = 1
                    obj.save()
        
        # Incrementar y guardar
        folio = str(obj.contador)
        obj.contador += 1
        obj.save()
        return folio


class Pago(models.Model):
    """Registra el método y detalles del pago de una venta"""
    METODOS_PAGO = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta Débito', 'Tarjeta Débito'),
        ('Tarjeta Crédito', 'Tarjeta Crédito'),
        ('Transferencia Bancaria', 'Transferencia Bancaria'),
        ('Pago Mixto', 'Pago Mixto'),
    ]
    
    venta = models.OneToOneField(Venta, on_delete=models.CASCADE, related_name='pago')
    metodo = models.CharField(max_length=30, choices=METODOS_PAGO)
    monto_recibido = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Efectivo
    vuelto = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    
    # Tarjeta
    numero_tarjeta = models.CharField(max_length=4, blank=True, help_text="Últimos 4 dígitos")
    banco = models.CharField(max_length=100, blank=True)
    
    # Transferencia
    numero_operacion = models.CharField(max_length=50, blank=True)
    banco_origen = models.CharField(max_length=100, blank=True)
    
    # Pago Mixto
    monto_efectivo = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    monto_tarjeta = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    monto_transferencia = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    
    fecha_pago = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Pago {self.id} - {self.metodo} - ${self.monto_recibido}"
