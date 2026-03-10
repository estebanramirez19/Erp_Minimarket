# contabilidad/views.py
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from .models import Gasto, SistemaCaja, Inversor, DetalleInversion
from .forms import (
    GastoForm,
    SistemaCajaForm,
    InversorForm,
    DetalleInversionForm,
)


@method_decorator(login_required, name="dispatch")
class GastoListView(ListView):
    model = Gasto
    template_name = "contabilidad/gasto_list.html"
    context_object_name = "gastos"
    ordering = ["-fecha"]  # usa tu campo fecha

@method_decorator(login_required, name="dispatch")
class GastoCreateView(CreateView):
    model = Gasto
    form_class = GastoForm
    template_name = "contabilidad/gasto_form.html"
    success_url = reverse_lazy("contabilidad:gasto_list")

@method_decorator(login_required, name="dispatch")
class GastoUpdateView(UpdateView):
    model = Gasto
    form_class = GastoForm
    template_name = "contabilidad/gasto_form.html"
    success_url = reverse_lazy("contabilidad:gasto_list")


@method_decorator(login_required, name="dispatch")
class CajaListView(ListView):
    model = SistemaCaja
    template_name = "contabilidad/caja_list.html"
    context_object_name = "cajas"
    ordering = ["-fecha_apertura"]


@method_decorator(login_required, name="dispatch")
class CajaUpdateView(UpdateView):
    model = SistemaCaja
    form_class = SistemaCajaForm
    template_name = "contabilidad/caja_form.html"
    success_url = reverse_lazy("contabilidad:caja_list")


@method_decorator(login_required, name="dispatch")
class InversorListView(ListView):
    model = Inversor
    template_name = "contabilidad/inversor_list.html"
    context_object_name = "inversores"
    ordering = ["nombre"]


@method_decorator(login_required, name="dispatch")
class InversorCreateView(CreateView):
    model = Inversor
    form_class = InversorForm
    template_name = "contabilidad/inversor_form.html"
    success_url = reverse_lazy("contabilidad:inversor_list")


@method_decorator(login_required, name="dispatch")
class InversorUpdateView(UpdateView):
    model = Inversor
    form_class = InversorForm
    template_name = "contabilidad/inversor_form.html"
    success_url = reverse_lazy("contabilidad:inversor_list")


@method_decorator(login_required, name="dispatch")
class DetalleInversionListView(ListView):
    model = DetalleInversion
    template_name = "contabilidad/inversion_list.html"
    context_object_name = "inversiones"
    ordering = ["-fecha"]


@method_decorator(login_required, name="dispatch")
class DetalleInversionCreateView(CreateView):
    model = DetalleInversion
    form_class = DetalleInversionForm
    template_name = "contabilidad/inversion_form.html"
    success_url = reverse_lazy("contabilidad:inversion_list")


@method_decorator(login_required, name="dispatch")
class DetalleInversionUpdateView(UpdateView):
    model = DetalleInversion
    form_class = DetalleInversionForm
    template_name = "contabilidad/inversion_form.html"
    success_url = reverse_lazy("contabilidad:inversion_list")
