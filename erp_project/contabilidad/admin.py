from django.contrib import admin

# Register your models here.
#Gastos, Sistema de Caja, Inversor, DetalleInversion y DescuentosPromocionales.
from .models import Gasto, SistemaCaja, Inversor, DetalleInversion

admin.site.register(Gasto)  # bd de administracion de gastos
admin.site.register(SistemaCaja)  # bd de administracion de sistema de caja
admin.site.register(Inversor)  # bd de administracion de inversores
admin.site.register(DetalleInversion)  # bd de administracion de detalles de inversion  





