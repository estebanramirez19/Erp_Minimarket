from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    ROLES = [
        ("Administrador", "Administrador"),
        ("Supervisor", "Supervisor"),
        ("Vendedor", "Vendedor"),
        ("Contador", "Contador"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=30, choices=ROLES, default='Vendedor')
    email = models.EmailField(unique=True, blank=True, null=True, default="")
    nombre = models.CharField(max_length=100, default="")
    apellido = models.CharField(max_length=100, default="")
    telefono = models.CharField(max_length=15, blank=True)
    contraseña = models.CharField(max_length=12, default="user123")
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    ultima_conexion = models.DateTimeField(null=True, blank=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    
