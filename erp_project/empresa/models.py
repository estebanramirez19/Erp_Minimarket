from django.db import models

# Create your models here.

class Empresa(models.Model):
    representante_legal = models.CharField(max_length=100, blank=True, help_text="Nombre del representante legal",  null=True)
    razon_social = models.CharField(max_length=200, blank=True, help_text="Razón social de la empresa",  null=True)
    rut = models.CharField(max_length=20, blank=True, help_text="RUT de la empresa",  null=True)
    giro = models.CharField(max_length=100, blank=True, help_text="Giro de la empresa",  null=True)
    direccion = models.CharField(max_length=255, blank=True, help_text="Dirección de la empresa",  null=True)    
    email = models.EmailField(blank=True, help_text="Correo electrónico de la empresa",  null=True)
    comuna = models.CharField(max_length=100, blank=True, help_text="Comuna de la empresa",  null=True)
    ciudad = models.CharField(max_length=100, blank=True, help_text="Ciudad de la empresa",  null=True)
    region = models.CharField(max_length=100, blank=True, help_text="Región de la empresa",  null=True)
    telefono = models.CharField(max_length=20, blank=True, help_text="Teléfono de la empresa",  null=True)
    logo = models.ImageField(upload_to='media/logos/', blank=True, null=True)
    fecha_fundacion = models.DateField(null=True, blank=True, help_text="Fecha de fundación de la empresa")
    numero_empleados = models.IntegerField(null=True, blank=True, help_text="Número de empleados de la empresa")

    class Meta:
        permissions = [
            ("view_empresa", "Can view empresa"),
            ("add_empresa", "Can add empresa"),
            ("change_empresa", "Can change empresa"),
            ("delete_empresa", "Can delete empresa"),
        ]