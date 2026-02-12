from django.db import models
from django.contrib.auth.models import User

class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=50)

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    codigo_barra = models.CharField(max_length=30, unique=True)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)

class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    

class LecturaCodigo(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    codigo = models.CharField(max_length=100)
    fecha_lectura = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # quien leyó
    dispositivo = models.CharField(max_length=100, blank=True)  # opcional: nombre/id dispositivo

    def __str__(self):
        return f"{self.codigo} ({self.fecha_lectura})"

class ImagenProducto(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/imagenes/')
    descripcion = models.CharField(max_length=255, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=30, blank=True, default="Reconocimiento")  # para diferenciar tipos de imagen

    def __str__(self):
        return f"Imagen de {self.producto.nombre} ({self.fecha_subida.date()})"