# ventas/urls.py
from django.urls import path
from . import views

app_name = "ventas"

urlpatterns = [
    # Crear venta (la principal que me mostraste)
    path("crear/", views.crear_venta, name="crear_venta"),

    # Historial de ventas (solo admin, pero URL normal)
    path("historial/", views.historial_ventas, name="historial_ventas"),

    # Lista de ventas (pantalla principal)
    path("/", views.lista_ventas, name="lista_ventas"),

    # Editar venta
    path("editar/<int:venta_id>/", views.editar_venta, name="editar_venta"),
]
