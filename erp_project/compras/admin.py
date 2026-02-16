from django.contrib import admin

# Register your models here.
from .models import Compra, DetalleCompra
admin.site.register(Compra) #bd de administracion de compras
admin.site.register(DetalleCompra) #bd de administracion de detalles de compras
