from django.urls import path
from . import views

app_name = 'compras'


##falta Reparar

urlpatterns = [
    path('', views.lista_compras, name='lista_compras'),
    path('crear/', views.crear_compra, name='crear_compra'),
    path('<int:compra_id>/', views.detalle_compra, name='detalle_compra'),
    path('<int:compra_id>/agregar-detalle/', views.agregar_detalle_manual, name='agregar_detalle_manual'),
    path('detalle/<int:detalle_id>/quitar/', views.quitar_detalle, name='quitar_detalle'),
    path('buscar-productos/', views.buscar_productos, name='buscar_productos'),
    path('procesar-pdf/', views.procesar_pdf_ajax, name='procesar_pdf_ajax'),
    path('agregar-detalle-temporal/', views.agregar_detalle_temporal, name='agregar_detalle_temporal'),
    path('agregar-detalles-temporales-batch/', views.agregar_detalles_temporales_batch, name='agregar_detalles_temporales_batch'),
    path('quitar-detalle-temporal/<int:detalle_temp_id>/', views.quitar_detalle_temporal, name='quitar_detalle_temporal'),
    path('agregar-detalle-edit/', views.agregar_detalle_edit, name='agregar_detalle_edit'),
    path('quitar-detalle-edit/<int:detalle_temp_id>/', views.quitar_detalle_edit, name='quitar_detalle_edit'),
    path('<int:compra_id>/editar/', views.editar_compra, name='editar_compra'),
    path('<int:compra_id>/eliminar/', views.eliminar_compra, name='eliminar_compra'),
]