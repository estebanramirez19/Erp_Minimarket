
from django.db import models
from django.contrib.auth.models import User

from empresa.models import Empresa


class UserProfile(models.Model):
    ROLES = [
        ('owner', 'Dueño'),
        ('administrador', 'Administrador'),
        ('supervisor', 'Supervisor'),
        ('empleado', 'Empleado'),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    rol = models.CharField(
        max_length=30, choices=ROLES, default='empleado'
    )
    telefono = models.CharField(max_length=15, blank=True)
    foto_perfil = models.ImageField(
        upload_to='fotos_perfil/', blank=True, null=True
    )
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    ultima_conexion = models.DateTimeField(blank=True, null=True)

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios',
    )

    # Para facilitar la lógica de “dueño de la empresa”
    es_dueno = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
        permissions = [
            ("can_view_dashboard", "Puede ver el dashboard"),
            ("can_manage_users", "Puede gestionar usuarios"),
            ("can_manage_products", "Puede gestionar productos"),
            ("can_manage_sales", "Puede gestionar ventas"),
            ("can_view_reports", "Puede ver reportes"),
        ]

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.rol})"