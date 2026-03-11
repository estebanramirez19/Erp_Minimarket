from django import forms
from django.forms import inlineformset_factory
from .models import Compra, DetalleCompra
from inventario.models import Inventario

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = "__all__"   # opcional: luego puedes limitar
        widgets = {
            "proveedor": forms.Select(attrs={"class": "form-control"}),
            "tipo_documento": forms.Select(attrs={"class": "form-control"}),
            "tipo_pago": forms.Select(attrs={"class": "form-control"}),
            # agrega aquí otros campos que muestras en el form
        }


class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ["inventario", "cantidad", "precio_unitario"]
        widgets = {
            "inventario": forms.Select(attrs={"class": "form-control"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "precio_unitario": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opcional: filtrar solo productos activos
        self.fields["inventario"].queryset = (
            Inventario.objects
            .select_related("producto")
            .filter(producto__activo=True)
            .order_by("producto__nombre")
        )

        # Si estás editando un detalle existente, no permitas cambiar el producto
        if self.instance.pk:
            self.fields["inventario"].widget = forms.HiddenInput()
        else:
            self.fields["inventario"].widget = forms.Select(attrs={"class": "form-control"})



DetalleCompraFormSet = inlineformset_factory(
    parent_model=Compra,
    model=DetalleCompra,
    form=DetalleCompraForm,
    extra=5,
    can_delete=True,
)
