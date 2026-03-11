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
    folio = models.CharField(max_length=20, unique=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo_documento = models.CharField(max_length=20, choices=TIPO_DOCUMENTO_CHOICES, default="BOLETA")
    tipo_pago = models.CharField(max_length=20, choices=TIPO_PAGO_CHOICES, default="EFECTIVO")

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ["-fecha", "-id"]  # ← corregido

    def calcular_totales(self, guardar=True):
        subtotal = sum(det.subtotal for det in self.detalles.all())
        iva = (subtotal * IVA_CHILE).quantize(Decimal("1"))
        total = subtotal + iva
        self.subtotal, self.iva, self.total = subtotal, iva, total
        if guardar:
            self.save(update_fields=["subtotal", "iva", "total"])
        return self.subtotal, self.iva, self.total

    def __str__(self):
        return f"Venta {self.id} Folio: {self.folio} - Razon Social: {self.empresa.razon_social} - RUT: {self.empresa.rut} - Giro: {self.empresa.giro}- Direccion: {self.empresa.direccion} - Comuna: {self.empresa.comuna} - Ciudad: {self.empresa.ciudad} - Fecha: {self.fecha.strftime('%Y-%m-%d %H:%M:%S')} - Metodo de Pago: {self.tipo_pago} -SubTotal: ${self.subtotal} - IVA: ${self.iva} - Total: ${self.total}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="detalles")
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, related_name="detalles_venta")
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    @property
    def subtotal(self):
        return self.precio_unitario * self.cantidad

    def __str__(self):
        return (
            f"Venta {self.venta.id} | "
            f"Codigo: {self.inventario.producto.id} | "
            f"Producto: {self.inventario.producto.nombre} | "
            f"Cantidad: {self.cantidad} | "
            f"Precio Unitario: ${self.precio_unitario} | "
            f"Subtotal: ${self.subtotal}"
        )


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
    venta = models.OneToOneField(Venta, on_delete=models.CASCADE, related_name="pago")

    # Datos genéricos
    tipo_pago = models.CharField(max_length=20, choices=TIPO_PAGO_CHOICES)

    # Efectivo
    monto_recibido = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    vuelto = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)

    # Tarjeta
    numero_tarjeta = models.CharField(max_length=4, blank=True)
    banco_tarjeta = models.CharField(max_length=30, blank=True)

    # Transferencia
    numero_operacion = models.CharField(max_length=50, blank=True)
    banco_origen = models.CharField(max_length=100, blank=True)

    # Mixto
    monto_efectivo = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    monto_tarjeta = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    monto_transferencia = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)

    fecha_pago = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago venta {self.venta_id} - {self.tipo_pago} - Total ${self.venta.total}"

   