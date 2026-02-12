from django.db import models
from proveedores.models import Proveedor
from inventario.models import Producto
from django.contrib.auth.models import User

class Compra(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='compras')

    
    tipo_documento = models.CharField(max_length=15, choices=[('Factura', 'Factura'), ('Boleta', 'Boleta'), ('Nota de Crédito', 'Nota de Crédito'),('Nota de Débito', 'Nota de Débito'), ('Sin Documento', 'Sin Documento')], default='Boleta')
    folio = models.CharField(max_length=30, blank=True)

    razon_social = models.CharField(max_length=200, blank=True, help_text="Razón social de la empresa")
    rut = models.CharField(max_length=20, blank=True, help_text="RUT de la empresa")
    giro = models.CharField(max_length=100, blank=True, help_text="Giro de la empresa")
    direccion = models.CharField(max_length=255, blank=True, help_text="Dirección de la empresa")    
    email = models.EmailField(blank=True, help_text="Correo electrónico de la empresa")
    Comuna = models.CharField(max_length=100, blank=True, help_text="Comuna de la empresa")
    ciudad = models.CharField(max_length=100, blank=True, help_text="Ciudad de la empresa")
    
    fecha_compra = models.DateField(null=True, blank=True, help_text="Fecha del documento")
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) #usuario que gestiona la compra
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    iva = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=0, default=0) 

    pdf = models.FileField(upload_to='media/pdfs/', blank=True, null=True)


class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  #aqui tengo que ir a el tema del inventario
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=0)

    def subtotal(self):        return self.cantidad * self.precio_unitario

class DevolucionCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='devoluciones')
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    motivo = models.TextField(blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    iva = models.DecimalField(max_digits=10, decimal_places=0, default=0
)
    total = models.DecimalField(max_digits=12, decimal_places=0, default=0)

class DetalleDevolucionCompra(models.Model):
    devolucion = models.ForeignKey(DevolucionCompra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=0)

    def subtotal(self):
        return self.cantidad * self.precio_unitario
    
class CambioCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='cambios')
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    motivo = models.TextField(blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    iva = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=0, default=0)

class DetalleCambioCompra(models.Model):
    cambio = models.ForeignKey(CambioCompra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=0)

    def subtotal(self):
        return self.cantidad * self.precio_unitario


