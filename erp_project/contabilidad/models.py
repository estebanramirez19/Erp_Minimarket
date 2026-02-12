from django.db import models

# Create your models here.
#Gastos, Sistema de Caja, Inversor, DetalleInversion y DescuentosPromocionales.
class Gasto(models.Model):
    descripcion = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    categoria = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return f"{self.descripcion} - {self.monto}"
    
class SistemaCaja(models.Model):
    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=0)
    saldo_actual = models.DecimalField(max_digits=12, decimal_places=0)
    cuenta_bancaria = models.CharField(max_length=100, blank=True)
    saldo_bancario = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    fecha_apertura = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=[('abierto', 'Abierto'), ('cerrado', 'Cerrado')], default='abierto')

    def __str__(self):
        return f"Caja - {self.estado} - Saldo Actual: {self.saldo_actual}"
    
class Inversor(models.Model):
    nombre = models.CharField(max_length=100)
    monto_invertido = models.DecimalField(max_digits=12, decimal_places=0)
    fecha_inversion = models.DateTimeField(auto_now_add=True)
    porcentaje_retorno = models.DecimalField(max_digits=5, decimal_places=0)

    def __str__(self):
        return f"{self.nombre} - Inversión: {self.monto_invertido}"
    
class DetalleInversion(models.Model):
    inversor = models.ForeignKey(Inversor, on_delete=models.CASCADE, related_name='detalles')
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=12, decimal_places=0)
    tipo_pago = models.CharField(max_length=20, choices=[('debito', 'debito'), ('capital', 'Capital')], default='interes')
    tipo_movimiento = models.CharField(max_length=20, choices=[('aporte', 'Aporte'), ('retiro', 'Retiro')], default='aporte')

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.monto} - {self.fecha}"
    
class DescuentoPromocional(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=255, blank=True)
    porcentaje_descuento = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo} - {self.porcentaje_descuento}%"