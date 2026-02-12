from django.urls import path
from . import views

app_name = 'empresa'
urlpatterns = [
    path('', views.empresa_view, name='empresa'),
    path('editar/', views.editar_empresa, name='editar_empresa'),
    path('eliminar/', views.eliminar_empresa, name='eliminar_empresa'),
    path('crear/', views.crear_empresa, name='crear_empresa'),
]