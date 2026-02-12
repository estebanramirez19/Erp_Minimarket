from django.urls import path
from . import views

app_name = 'ventas'

##hay que adaptarlo

urlpatterns = [
    path('crear/', views.crear_venta, name='crear_venta'),

    path('agregar/manual/<int:venta_id>/', views.agregar_producto_manual, name='agregar_producto_manual'),
    path('agregar/codigo/<int:venta_id>/', views.agregar_producto_por_codigo, name='agregar_producto_codigo'),
    path('quitar-producto/<int:detalle_id>/', views.quitar_producto, name='quitar_producto'),
    path('precio-por-peso/<int:venta_id>/', views.precio_por_peso, name='precio_por_peso'),
    path('historial/', views.historial_ventas, name='historial_ventas'),
    path('editar/<int:venta_id>/', views.editar_venta, name='editar_venta'),
    path('cancelar/<int:venta_id>/', views.cancelar_venta, name='cancelar_venta'),
    path('finalizar-venta/<int:venta_id>/', views.finalizar_venta, name='finalizar_venta'),
    path('promociones/nueva/', views.crear_promocion, name='crear_promocion'),
    path('aplicar-descuento/<int:venta_id>/', views.aplicar_descuento, name='aplicar_descuento'),
    path('seleccionar-medio-pago/<int:venta_id>/', views.seleccionar_medio_pago, name='seleccionar_medio_pago'),
    path('<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
    path('', views.lista_ventas, name='lista_ventas'),
    
]
