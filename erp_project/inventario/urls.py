from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.datos_producto, name='datos_producto'),
    path('<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path("categoria/crear/", views.crear_categoria, name="crear_categoria"),
]
