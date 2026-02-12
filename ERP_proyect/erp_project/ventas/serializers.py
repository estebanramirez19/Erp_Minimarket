from rest_framework import serializers
from .models import Venta, DetalleVenta  # Descuento

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = '__all__'
        
# class DescuentoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Descuento
#         fields = '__all__'