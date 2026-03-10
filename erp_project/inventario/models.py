from django.db import models

class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to="media/productos/", blank=True, null=True)
    codigo_barra = models.CharField(max_length=30, unique=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=0)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - {self.categoria.nombre} - Precio Venta: {self.precio_venta} - Precio Compra: {self.precio_compra} - Activo: {'Sí' if self.activo else 'No'} - Código de Barra: {self.codigo_barra}"


class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Inventario de {self.producto.nombre} - Cantidad: {self.cantidad} - Última actualización: {self.fecha_actualizacion.strftime('%Y-%m-%d %H:%M:%S')}"


class AjustesInventario(models.Model):
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    cantidad_ajustada = models.IntegerField()
    motivo = models.CharField(
        max_length=10, choices=[
            ('Robos', 'Robos'), 
            ('Mermas', 'Mermas'), 
            ('Extravios', 'Extravios')])
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=0)
    tipo_ajuste = models.CharField(
        max_length=10,
        choices=[
            ('Entrada', 'Entrada'),
            ('Salida', 'Salida')
        ]
    )

    def __str__(self):
        return f"Ajuste {self.motivo} - {self.descripcion} - {self.tipo_ajuste} - {self.inventario.producto.nombre} - {self.cantidad_ajustada} - {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}"
