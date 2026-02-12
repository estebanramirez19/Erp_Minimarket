from django.contrib import admin
from .models import Venta, DetalleVenta, FolioCounter, Pago  # Descuento

admin.site.register(Venta)  # bd de administracion de ventas
admin.site.register(DetalleVenta)  # bd de administracion de detalles de venta
admin.site.register(FolioCounter)  # bd de administración de contadores de folio
admin.site.register(Pago)  # bd de administración de pagos
 # bd de administracion de descuentos

# Register your models here.
