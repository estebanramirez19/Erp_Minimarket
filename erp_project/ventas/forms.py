from django import forms
from .models import Venta, DetalleVenta 

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'  

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields =[ 'Producto', 'cantidad', 'precio_unitario' ]
        widgets = {
            'Producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Lógica condicional para producto
        if self.instance.pk:  # Editando existente
            self.fields['Producto'].widget = forms.HiddenInput()
            self.fields['Producto'].initial = self.instance.producto_id  # Solo ID
        else:  # permite seleccionar o escribir nuevo
            self.fields['Producto'].widget = forms.TextInput(attrs={'class': 'form-control'})

DetalleVentaFormSet =  forms.inlineformset_factory(
    parent_model=Venta,
    model=DetalleVenta,
    form=DetalleVentaForm, #aqui se asigna el formulario personalizado
    extra=5,
    can_delete=True,
)