from django.db import models

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=15, blank=True, null=True)
    giro = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    activo = models.BooleanField(default=True)
