from django.contrib import admin

# Register your models here.
from .models import Compra, DetalleCompra, DevolucionCompra, DetalleDevolucionCompra, CambioCompra, DetalleCambioCompra
admin.site.register(Compra) #bd de administracion de compras
admin.site.register(DetalleCompra) #bd de administracion de detalles de compras
admin.site.register(DevolucionCompra) #bd de administracion de devoluciones de compras
admin.site.register(DetalleDevolucionCompra) #bd de administracion de detalles de devoluciones de compras
admin.site.register(CambioCompra) #bd de administracion de cambios de compras