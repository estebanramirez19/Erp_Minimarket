from django.db import models
from django.contrib.auth.models import User
from proveedores.models import Proveedor
from inventario.models import Producto
from decimal import Decimal


IVA_CHILE = Decimal("0.19")


class Compra(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ("FACTURA", "Factura"),
        ("BOLETA", "Boleta"),
        ("NC", "Nota de Crédito"),
        ("ND", "Nota de Débito"),
        ("SD", "Sin Documento"),
    ]

    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name="compras",
    )

    tipo_documento = models.CharField(
        max_length=10,
        choices=TIPO_DOCUMENTO_CHOICES,
        default="FACTURA",
    )
    folio = models.CharField(max_length=30, blank=True)

    # Si quieres histórico inmutable del proveedor en la compra:
    razon_social_proveedor = models.CharField(
        max_length=200,
        blank=True,
        help_text="Razón social del proveedor al momento de la compra",
    )
    rut_proveedor = models.CharField(
        max_length=20,
        blank=True,
        help_text="RUT del proveedor al momento de la compra",
    )
    giro_proveedor = models.CharField(max_length=100, blank=True)
    direccion_proveedor = models.CharField(max_length=255, blank=True)
    email_proveedor = models.EmailField(blank=True)
    comuna_proveedor = models.CharField(max_length=100, blank=True)
    ciudad_proveedor = models.CharField(max_length=100, blank=True)

    fecha_compra = models.DateField(null=True, blank=True)

    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="compras_registradas",
    )
    empresa = models.CharField(max_length=100, blank=True)

    razon_social_empresa = models.CharField(
        max_length=200,
        blank=True,
        help_text="Razón social de la empresa al momento de la compra",
    )
    rut_empresa = models.CharField(
        max_length=20,
        blank=True,
        help_text="RUT de la empresa al momento de la compra",
    )
    
    giro_empresa = models.CharField(max_length=100, blank=True)
    direccion_empresa = models.CharField(max_length=255, blank=True)
    email_empresa = models.EmailField(blank=True)
    comuna_empresa = models.CharField(max_length=100, blank=True)
    ciudad_empresa = models.CharField(max_length=100, blank=True)


    # Montos en pesos (entero); si quieres decimales, usa decimal_places=2
    subtotal = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    iva = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    total = models.DecimalField(max_digits=14, decimal_places=0, default=0)

    pdf = models.FileField(upload_to="compras/pdfs/", blank=True, null=True)

    class Meta:
        ordering = ["-fecha_compra", "-id"]

    def __str__(self):
        return f"Compra #{self.id} - {self.proveedor}"

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


class DetalleCompra(models.Model):
    compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        related_name="detalles",
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name="detalles_compra",
    )
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=0)

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"
