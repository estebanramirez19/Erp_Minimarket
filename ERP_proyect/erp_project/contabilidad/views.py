from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Gasto, SistemaCaja, Inversor, DetalleInversion, DescuentoPromocional

# Gasto CRUD
class GastoList(ListView):
    model = Gasto

class GastoDetail(DetailView):
    model = Gasto

class GastoCreate(CreateView):
    model = Gasto
    fields = ['descripcion', 'monto', 'categoria']
    success_url = reverse_lazy('gasto_list')

class GastoUpdate(UpdateView):
    model = Gasto
    fields = ['descripcion', 'monto', 'categoria']
    success_url = reverse_lazy('gasto_list')

class GastoDelete(DeleteView):
    model = Gasto
    success_url = reverse_lazy('gasto_list')

# SistemaCaja CRUD
class SistemaCajaList(ListView):
    model = SistemaCaja

class SistemaCajaDetail(DetailView):
    model = SistemaCaja

class SistemaCajaCreate(CreateView):
    model = SistemaCaja
    fields = ['saldo_inicial', 'saldo_actual', 'cuenta_bancaria', 'saldo_bancario', 'estado']
    success_url = reverse_lazy('sistemacaja_list')

class SistemaCajaUpdate(UpdateView):
    model = SistemaCaja
    fields = ['saldo_inicial', 'saldo_actual', 'cuenta_bancaria', 'saldo_bancario', 'estado']
    success_url = reverse_lazy('sistemacaja_list')

class SistemaCajaDelete(DeleteView):
    model = SistemaCaja
    success_url = reverse_lazy('sistemacaja_list')

# Inversor CRUD
class InversorList(ListView):
    model = Inversor

class InversorDetail(DetailView):
    model = Inversor

class InversorCreate(CreateView):
    model = Inversor
    fields = ['nombre', 'monto_invertido', 'porcentaje_retorno']
    success_url = reverse_lazy('inversor_list')

class InversorUpdate(UpdateView):
    model = Inversor
    fields = ['nombre', 'monto_invertido', 'porcentaje_retorno']
    success_url = reverse_lazy('inversor_list')

class InversorDelete(DeleteView):
    model = Inversor
    success_url = reverse_lazy('inversor_list')

# DetalleInversion CRUD
class DetalleInversionList(ListView):
    model = DetalleInversion

class DetalleInversionDetail(DetailView):
    model = DetalleInversion

class DetalleInversionCreate(CreateView):
    model = DetalleInversion
    fields = ['inversor', 'monto', 'tipo_pago', 'tipo_movimiento']
    success_url = reverse_lazy('detalleinversion_list')

class DetalleInversionUpdate(UpdateView):
    model = DetalleInversion
    fields = ['inversor', 'monto', 'tipo_pago', 'tipo_movimiento']
    success_url = reverse_lazy('detalleinversion_list')

class DetalleInversionDelete(DeleteView):
    model = DetalleInversion
    success_url = reverse_lazy('detalleinversion_list')

# DescuentoPromocional CRUD
class DescuentoPromocionalList(ListView):
    model = DescuentoPromocional

class DescuentoPromocionalDetail(DetailView):
    model = DescuentoPromocional

class DescuentoPromocionalCreate(CreateView):
    model = DescuentoPromocional
    fields = ['codigo', 'descripcion', 'porcentaje_descuento', 'fecha_inicio', 'fecha_fin', 'activo']
    success_url = reverse_lazy('descuentopromocional_list')

class DescuentoPromocionalUpdate(UpdateView):
    model = DescuentoPromocional
    fields = ['codigo', 'descripcion', 'porcentaje_descuento', 'fecha_inicio', 'fecha_fin', 'activo']
    success_url = reverse_lazy('descuentopromocional_list')

class DescuentoPromocionalDelete(DeleteView):
    model = DescuentoPromocional
    success_url = reverse_lazy('descuentopromocional_list')
