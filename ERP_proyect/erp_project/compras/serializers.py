from rest_framework import serializers
from .models import CambioCompra, Compra, DetalleCompra, DevolucionCompra

class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = '__all__'

class DetalleCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleCompra
        fields = '__all__'

class DevolucionCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevolucionCompra
        fields = '__all__'

class DetalleDevolucionCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevolucionCompra
        fields = '__all__'

class CambioCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = CambioCompra
        fields = '__all__'

class DetalleCambioCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = CambioCompra
        fields = '__all__'
