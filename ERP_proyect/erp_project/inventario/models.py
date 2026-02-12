from django.db import models

class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='media/productos/', blank=True, null=True)
    codigo_barra = models.CharField(max_length=30, unique=True)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=0)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Inventario de {self.producto.nombre}"


class Mermas(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    motivo = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Merma: {self.producto.nombre} ({self.cantidad})"


class Robos(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Robo: {self.producto.nombre} ({self.cantidad})"


class Extravios(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Extravio: {self.producto.nombre} ({self.cantidad})"


class AjustesInventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_ajustada = models.IntegerField()
    motivo = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    tipo_ajuste = models.CharField(
        max_length=10,
        choices=[
            ('Entrada', 'Entrada'),
            ('Salida', 'Salida')
        ]
    )

    def __str__(self):
        return f"Ajuste {self.tipo_ajuste} - {self.producto.nombre}"
