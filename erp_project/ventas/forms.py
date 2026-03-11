from django import forms
from .models import Venta, DetalleVenta 
from django.forms import inlineformset_factory

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ["empresa", "cliente", "tipo_documento", "tipo_pago"]  # vendedor, totales se setean en la view
        widgets = {
            "empresa": forms.Select(attrs={"class": "form-control"}),
            "cliente": forms.Select(attrs={"class": "form-control"}),
            "tipo_documento": forms.Select(attrs={"class": "form-control"}),
            "tipo_pago": forms.Select(attrs={"class": "form-control"}),
        }


class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ["inventario", "cantidad", "precio_unitario"]
        widgets = {
            "inventario": forms.Select(attrs={"class": "form-control"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "precio_unitario": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Editando un detalle existente: no permitir cambiar producto
            self.fields["inventario"].widget = forms.HiddenInput()
        else:
            # Nuevo detalle: desplegar selector
            self.fields["inventario"].widget = forms.Select(attrs={"class": "form-control"})

DetalleVentaFormSet = inlineformset_factory(
    parent_model=Venta,
    model=DetalleVenta,
    form=DetalleVentaForm,
    extra=5,
    can_delete=True,
)
