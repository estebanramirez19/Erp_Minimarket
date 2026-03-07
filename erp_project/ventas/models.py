from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from clientes.models import Cliente
from inventario.models import Inventario
from empresa.models import Empresa

IVA_CHILE = Decimal("0.19")
TIPO_PAGO_CHOICES = [
    ("EFECTIVO", "Efectivo"),
    ("TRANSFERENCIA", "Transferencia"),
    ("CHEQUE", "Cheque"),
    ("DEBITO", "TarjetaDébito"),
    ("CREDITO", "TarjetaCrédito"),
    ("MIXTO", "Mixto"),
    ("OTRO", "Otro"),
]
TIPO_DOCUMENTO_CHOICES = [
    ("FACTURA", "Factura"),
    ("BOLETA", "Boleta"),
    ("NC", "Nota de Crédito"),
    ("ND", "Nota de Débito"),
    ("SD", "Sin Documento"),
]

class Venta(models.Model): 
    folio = models.CharField(max_length=30, blank=True)
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)  # Relación con Empresa para datos
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True) #relacion con cliente, puede ser null si es una venta a un cliente ocasional o sin registro, pero si es a un cliente registrado, no puede ser null
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL) #relacion con account para autenticar, puede ser null si se borra el usuario, pero si el usuario existe, no puede ser null
    
    fecha = models.DateTimeField(auto_now_add=True)

    tipo_documento = models.CharField(
        max_length=20, 
        choices=TIPO_DOCUMENTO_CHOICES, 
        default='BOLETA'
    )

    tipo_pago = models.CharField(
        max_length=20,
        choices=TIPO_PAGO_CHOICES,
        default='EFECTIVO'
    )

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pdf = models.FileField(upload_to='media/ventas/pdfs/', blank=True, null=True)

    class Meta:
        ordering = ["-fecha_compra", "-id"]

    def calcular_totales(self, guardar=True):
        subtotal = sum(
            detalle.subtotal for detalle in self.detalles.all()
        )
        iva = (subtotal * IVA_CHILE).quantize(Decimal("1"))
        total = subtotal + iva

        self.subtotal = subtotal
        self.iva = iva
        self.total = total

        if guardar:
            self.save(update_fields=["subtotal", "iva", "total"])

        return self.subtotal, self.iva, self.total

    def __str__(self):
        return f"Venta {self.id} Folio: {self.folio} - Razon Social: {self.empresa.razon_social} - RUT: {self.empresa.rut} - Giro: {self.empresa.giro}- Direccion: {self.empresa.direccion} - Comuna: {self.empresa.comuna} - Ciudad: {self.empresa.ciudad} - Fecha: {self.fecha.strftime('%Y-%m-%d %H:%M:%S')} - Metodo de Pago: {self.tipo_pago} -SubTotal: ${self.subtotal} - IVA: ${self.iva} - Total: ${self.total}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, related_name='detalles_venta')

    @property
    def subtotal(self):
        return self.inventario.producto.precio_venta * self.inventario.cantidad 
    
    def __str__(self):
        return f"Venta {self.venta.id} Codigo: {self.inventario.producto.id} | Producto: {self.inventario.producto.nombre} | Cantidad: {self.inventario.cantidad} | Precio Unitario: ${self.inventario.producto.precio_venta} | Subtotal: ${self.subtotal}"


class FolioCounter(models.Model):
    #Contador de folios por tipo de documento
    tipo_documento = models.CharField(
        max_length=20,
        choices=TIPO_DOCUMENTO_CHOICES,
        unique=True
    )
    contador = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.tipo_documento}: {self.contador}"
    
    class Meta:
        verbose_name_plural = "Folio Counters"
    
    @classmethod
    def obtener_proximo_folio(cls, tipo_documento):
        #Obtiene el próximo folio para un tipo de documento, creando el contador si no existe
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
    venta = models.OneToOneField(Venta, on_delete=models.CASCADE, related_name='pago')

    if venta.tipo_pago == "EFECTIVO": # Efectivo
        monto_recibido = models.DecimalField(max_digits=12, decimal_places=0, default=0)
        vuelto = models.DecimalField(max_digits=12, decimal_places=0, default=0, null=True, blank=True)
    
    elif venta.tipo_pago == "DEBITO" or venta.tipo_pago == "CREDITO": #Tarjeta
        numero_tarjeta = models.CharField(max_length=4, blank=True, help_text="Últimos 4 dígitos")
        banco = models.CharField(max_length=30, blank=True)
  
    elif venta.tipo_pago == "TRANSFERENCIA": # Transferencia
        numero_operacion = models.CharField(max_length=50, blank=True)
        banco_origen = models.CharField(max_length=100, blank=True)
    
    elif venta.tipo_pago == "MIXTO": # Mixto
        monto_efectivo = models.DecimalField(max_digits=12, decimal_places=0, default=0, null=True, blank=True)
        monto_tarjeta = models.DecimalField(max_digits=12, decimal_places=0, default=0, null=True, blank=True)
        monto_transferencia = models.DecimalField(max_digits=12, decimal_places=0, default=0, null=True, blank=True)

    fecha_pago = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Pago {self.venta.id} - Metodo de Pago: {self.venta.tipo_pago} -Total ${self.venta.total} - Fecha: {self.fecha_pago.strftime('%Y-%m-%d %H:%M:%S')}"
