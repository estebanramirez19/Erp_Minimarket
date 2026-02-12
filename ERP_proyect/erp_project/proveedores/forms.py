from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        witgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proveedor'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12345678-9'}),
            'giro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Comercial de productos'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección del proveedor'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email del proveedor'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono del proveedor'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }