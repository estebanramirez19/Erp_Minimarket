from django.db import models
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

class Gasto(models.Model): #para gastos como cuentas de servicios, sueldos, etc.
    descripcion = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    categoria = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return f"{self.descripcion} - {self.monto}"
    
class SistemaCaja(models.Model):
    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=0)
    saldo_actual = models.DecimalField(max_digits=12, decimal_places=0)
    ingreso = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    egreso = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    cuenta_bancaria = models.CharField(max_length=100, blank=True)
    saldo_bancario = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    fecha_apertura = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=[("abierto", "Abierto"), ("cerrado", "Cerrado")],
        default="abierto",
    )
    def actualizar_saldo(self, monto, tipo_movimiento):
        if tipo_movimiento == 'ingreso':
            self.saldo_actual += monto
        elif tipo_movimiento == 'egreso':
            self.saldo_actual -= monto
        self.save()

    def get_caja_actual():
        try:
            return SistemaCaja.objects.get(estado="abierto")
        except ObjectDoesNotExist:
            return None

    def __str__(self):
        return f"Caja - {self.estado} - Saldo Actual: {self.saldo_actual}"
    
class Inversor(models.Model): #para registrar a los inversores, sus aportes y retornos
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(blank=True)

    def __str__(self):
        return f"Nombre:{self.nombre} - RUT: {self.rut} - Tel: {self.telefono} - Correo: {self.correo}"
    
class DetalleInversion(models.Model):
    inversor = models.ForeignKey(Inversor, on_delete=models.CASCADE, related_name='detalles')
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=12, decimal_places=0)
    tipo_pago = models.CharField(max_length=20, choices=[('debito', 'debito'), ('capital', 'Capital')], default='interes')
    tipo_movimiento = models.CharField(max_length=20, choices=[('aporte', 'Aporte'), ('retiro', 'Retiro')], default='aporte')

    def __str__(self):
        return f"Nombre: {self.inversor.nombre} - Monto: {self.monto} - Tipo Pago: {self.tipo_pago} - Tipo Movimiento: {self.tipo_movimiento}"
    

#    Aun no
# class DescuentoPromocional(models.Model):
#     para gestionar descuentos promocionales
#     codigo = models.CharField(max_length=50, unique=True)
#     descripcion = models.CharField(max_length=255, blank=True)
#     porcentaje_descuento = models.DecimalField(max_digits=5, decimal_places=2)
#     fecha_inicio = models.DateTimeField()
#     fecha_fin = models.DateTimeField()
#     activo = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.codigo} - {self.porcentaje_descuento}%"