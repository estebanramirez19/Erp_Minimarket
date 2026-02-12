from django.contrib import admin

# Register your models here.
from .models import Producto, CategoriaProducto , Inventario

admin.site.register(Producto) #bd de administracion de productos
admin.site.register(CategoriaProducto) #bd de administracion de categorias de productos
admin.site.register(Inventario) #bd de administracion de inventario

