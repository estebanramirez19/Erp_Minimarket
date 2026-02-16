from django import forms
from django.forms import inlineformset_factory
from .models import Compra, DetalleCompra


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = [
            "proveedor",
            "tipo_documento",
            "folio",
            "fecha_compra",
            "empresa",
            "razon_social_proveedor",
            "rut_proveedor",
            "giro_proveedor",
            "direccion_proveedor",
            "email_proveedor",
            "comuna_proveedor",
            "ciudad_proveedor",
            "razon_social_empresa",
            "rut_empresa",
            "giro_empresa",
            "direccion_empresa",
            "email_empresa",
            "comuna_empresa",
            "ciudad_empresa",
            "pdf",
        ]


DetalleCompraFormSet = inlineformset_factory(
    parent_model=Compra,
    model=DetalleCompra,
    fields=["producto", "cantidad", "precio_unitario"],
    extra=1,
    can_delete=True,
)
