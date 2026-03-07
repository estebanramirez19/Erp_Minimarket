from django import forms
from django.forms import inlineformset_factory
from .models import Compra, DetalleCompra


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ["__all__"]


class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ["producto", "cantidad", "precio_unitario"]  # Quita "id"
        widgets = {
            "producto": forms.Select(attrs={"class": "form-control"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "precio_unitario": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Lógica condicional para producto
        if self.instance.pk:  # Editando existente
            self.fields["producto"].widget = forms.HiddenInput()
            self.fields["producto"].initial = self.instance.producto_id  # Solo ID
        else:  # permite seleccionar o escribir nuevo
            self.fields["producto"].widget = forms.TextInput(attrs={"class": "form-control"})
            


DetalleCompraFormSet = inlineformset_factory(
    parent_model=Compra,
    model=DetalleCompra,
    form=DetalleCompraForm, #aqui se asigna el formulario personalizado
    extra=5,
    can_delete=True,
)