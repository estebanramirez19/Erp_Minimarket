# integrations/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('lector-codigo/', views.lector_codigo, name='lector_codigo'),
    # path('reconocer-imagen/', views.reconocimiento_producto_por_imagen, name='reconocer_imagen'),
]