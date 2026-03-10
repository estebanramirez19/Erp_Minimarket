# contabilidad/forms.py
from django import forms
from .models import Gasto, SistemaCaja, Inversor, DetalleInversion


class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ["descripcion", "monto", "categoria"]


class SistemaCajaForm(forms.ModelForm):
    class Meta:
        model = SistemaCaja
        fields = [
            "saldo_inicial",
            "saldo_actual",
            "Ingreso",
            "Egreso",
            "cuenta_bancaria",
            "saldo_bancario",
            "estado",
        ]


class InversorForm(forms.ModelForm):
    class Meta:
        model = Inversor
        fields = ["nombre", "rut", "telefono", "correo"]


class DetalleInversionForm(forms.ModelForm):
    class Meta:
        model = DetalleInversion
        fields = ["inversor", "monto", "tipo_pago", "tipo_movimiento"]
