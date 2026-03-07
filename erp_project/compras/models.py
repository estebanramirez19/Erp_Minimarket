from django.db import models
from django.contrib.auth.models import User
from proveedores.models import Proveedor
from inventario.models import Inventario, Producto
from empresa.models import Empresa
from decimal import Decimal


IVA_CHILE = Decimal("0.19")

##desde contabilidad debo hacer una view que se genere automaticamente cada vez que se registre una compra, con los datos de la compra 
# y el asiento contable asociado, para que se pueda llevar un control de las compras y su impacto en la contabilidad de la empresa.

class Compra(models.Model):  #tiene que estar relacionada con Proveedor, inventario, contabilidad y account para autenticar
    TIPO_DOCUMENTO_CHOICES = [
        ("FACTURA", "Factura"),
        ("BOLETA", "Boleta"),
        ("NC", "Nota de Crédito"),
        ("ND", "Nota de Débito"),
        ("SD", "Sin Documento"),
    ]
    TIPO_PAGO_CHOICES = [
        ("EFECTIVO", "Efectivo"),
        ("TRANSFERENCIA", "Transferencia"),
        ("CHEQUE", "Cheque"),
        ("DEBITO", "TarjetaDébito"),
        ("CREDITO", "TarjetaCrédito"),
        ("CHEQUE A FECHA", "Cheque a Fecha"),
        ("OTRO", "Otro"),
    ]

    proveedor = models.ForeignKey(   #proveedor, puede ser null si es una compra a un almacén o ambulante, pero si es a un proveedor registrado, no puede ser null
        Proveedor,
        on_delete=models.PROTECT,
        related_name="compras",
        blank=True,
    )

    tipo_documento = models.CharField(
        max_length=10,
        choices=TIPO_DOCUMENTO_CHOICES,
        default="FACTURA",
    )
    folio = models.CharField(max_length=30, blank=True)

    # necesario para cuando son compras mas simples como a almacenes o ambulantes 

    nombre_negocio = models.CharField(max_length=200, blank=True, null=True,)
    rut_negocio = models.CharField(max_length=20, blank=True, null=True)
    giro_negocio = models.CharField(max_length=100, null=True, blank=True)
    direccion_negocio = models.CharField(max_length=255, null=True, blank=True)
    comuna_negocio = models.CharField(max_length=100, null=True, blank=True)
    ciudad_negocio = models.CharField(max_length=100, null=True, blank=True)

    #aqui se vuelve a datos de factura comunes

    fecha_compra = models.DateField(blank=True)

    usuario = models.ForeignKey(                   ## Account OK
        User,
        on_delete=models.PROTECT,
        related_name="compras_registradas",
    )

    #que se llene automatico con los datos que estan registrados en el usuario
    empresa = models.ForeignKey(                  ## Empresa OK
        Empresa,
        on_delete=models.PROTECT,
        related_name="compras",
    )

    # Montos en pesos (entero); si quieres decimales, usa decimal_places=2
    subtotal = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    iva = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    total = models.DecimalField(max_digits=14, decimal_places=0, default=0)

    pdf = models.FileField(upload_to="media/compras/pdfs/", blank=True, null=True)
    metodo_pago = models.CharField(
        max_length=20,
        choices=TIPO_PAGO_CHOICES,
        default="EFECTIVO",
    )

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
        return f"ID Compra: {self.id}- Folio: {self.folio} - Tipo de Documento: {self.tipo_documento} - Proveedor: {self.proveedor.nombre if self.proveedor else self.nombre_negocio} - Rut Proveedor: {self.proveedor.rut if self.proveedor else self.rut_negocio} - Giro: {self.proveedor.giro if self.proveedor else self.giro_negocio} - Direccion: {self.proveedor.direccion if self.proveedor else self.direccion_negocio}- Comuna: {self.proveedor.comuna if self.proveedor else self.comuna_negocio} - Ciudad: {self.proveedor.ciudad if self.proveedor else self.ciudad_negocio}- Fecha: {self.fecha_compra.strftime('%Y-%m-%d') if self.fecha_compra else 'N/A'} - Razon Social: {self.empresa.razon_social} - Rut: {self.empresa.rut} - Giro: {self.empresa.giro} - Direccion: {self.empresa.direccion} - Comuna: {self.empresa.comuna} - Ciudad: {self.empresa.ciudad} - Subtotal: {self.subtotal} - IVA: {self.iva} - Total: {self.total} - Metodo de Pago: {self.metodo_pago}"


class DetalleCompra(models.Model):
    compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        related_name="detalles",
    )
    inventario = models.ForeignKey(
        Inventario,
        on_delete=models.PROTECT,
        related_name="detalles_compra",
    )

    @property
    def subtotal(self):
        return self.producto.precio_compra * self.inventario.cantidad

    def __str__(self):
        return f"Codigo: {self.producto.id} | Producto: {self.producto.nombre} | Cantidad: {self.inventario.cantidad} | Subtotal: {self.subtotal}"