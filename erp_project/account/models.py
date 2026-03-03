from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Perfil de usuario extendido que vincula campos adicionales con Django's User model
    """
    ROLES = [
        ('Administrador', 'Administrador'),
        ('Supervisor', 'Supervisor'),
        ('Vendedor', 'Vendedor'),
        ('Contador', 'Contador'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    rol = models.CharField(max_length=30, choices=ROLES, default='Vendedor')
    telefono = models.CharField(max_length=15, blank=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    ultima_conexion = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.rol})"


# Señal para crear automáticamente un perfil cuando se crea un usuario
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crea automáticamente un UserProfile cuando se crea un User"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Guarda automáticamente el UserProfile cuando se guarda el User"""
    instance.profile.save()
