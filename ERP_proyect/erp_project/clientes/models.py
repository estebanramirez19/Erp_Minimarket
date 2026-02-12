from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15, blank=True)
    activo = models.BooleanField(default=True)
