from django.contrib import admin
from .models import LecturaCodigo, ImagenProducto

@admin.register(LecturaCodigo)
class LecturaCodigoAdmin(admin.ModelAdmin):
    list_display = ("id", "producto", "codigo", "fecha_lectura")
    search_fields = ("codigo", "producto__nombre")
    list_filter = ("fecha_lectura",)
    raw_id_fields = ("producto",)

@admin.register(ImagenProducto)
class ImagenProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "producto", "imagen", "fecha_subida")
    search_fields = ("producto__nombre",)
    readonly_fields = ("fecha_subida",)
    raw_id_fields = ("producto",)
