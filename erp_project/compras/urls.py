from django.urls import path
from . import views

app_name = "compras"

urlpatterns = [
    # Lista principal
    path("", views.lista_compras, name="lista_compras"),
    
    # CRUD completo
    path("crear/", views.compra_crear, name="crear"),
    path("<int:compra_id>/", views.detalle_compra, name="detalle"),
    path("<int:compra_id>/editar/", views.editar_compra, name="editar"),
    path("<int:compra_id>/eliminar/", views.eliminar_compra, name="eliminar"),
    
    # AJAX
    path("productos/buscar/", views.buscar_productos, name="buscar_productos"),
]
