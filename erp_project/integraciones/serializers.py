from rest_framework import serializers
from .models import LecturaCodigo, ImagenProducto

class LecturaCodigoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturaCodigo
        fields = '__all__'

class ImagenProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenProducto
        fields = '__all__'


