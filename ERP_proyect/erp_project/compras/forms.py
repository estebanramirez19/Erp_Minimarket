from django import forms
from django.forms import inlineformset_factory

from erp_project.proveedores.models import Proveedor

from .models import (
    Compra,
    DetalleCompra,
    DevolucionCompra,
    DetalleDevolucionCompra,
    CambioCompra,
    DetalleCambioCompra,
)


# -------------------------
# COMPRA + DETALLECOMPRA
# -------------------------

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra, DetalleCompra, Proveedor
        fields = ['__all__'   
        ]



class CompraFormSet(forms.ModelForm):
    class Meta:
        model = Compra
        fields = '__all__'


class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields =  '__all__'



DetalleCompraFormSet = inlineformset_factory(
    Compra,
    DetalleCompra,
    form=DetalleCompraForm,
    extra=1,
    can_delete=True
)


# -------------------------
# DEVOLUCIÓN DE COMPRA
# -------------------------

class DevolucionCompraForm(forms.ModelForm):
    class Meta:
        model = DevolucionCompra
        fields =  '__all__'

class DevolucionCompraFormSet(forms.ModelForm):
    class Meta:
        model = DevolucionCompra
        fields = '__all__'


class DetalleDevolucionCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleDevolucionCompra
        fields =  '__all__'


DetalleDevolucionCompraFormSet = inlineformset_factory(
    DevolucionCompra,
    DetalleDevolucionCompra,
    form=DetalleDevolucionCompraForm,
    extra=1,
    can_delete=True
)


# -------------------------
# CAMBIO DE COMPRA
# -------------------------

class CambioCompraForm(forms.ModelForm):
    class Meta:
        model = CambioCompra
        fields =  '__all__'


class CambioCompraFormSet(forms.ModelForm):
    class Meta:
        model = CambioCompra
        fields = '__all__'


class DetalleCambioCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCambioCompra
        fields = '__all__'


DetalleCambioCompraFormSet = inlineformset_factory(
    CambioCompra,
    DetalleCambioCompra,
    form=DetalleCambioCompraForm,
    extra=1,
    can_delete=True
)
