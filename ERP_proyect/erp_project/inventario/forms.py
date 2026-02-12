from django import forms
from .models import Producto, CategoriaProducto, Inventario

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        
class CategoriaProductoForm(forms.ModelForm):
    class Meta:
        model = CategoriaProducto
        fields = '__all__'

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = '__all__'
