from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import models
from empresa.models import Empresa
from .models import Empresa
from .forms import EmpresaForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required ,permission_required

@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required('empresa.view_empresa', raise_exception=True), name="dispatch")
def empresa_view(request):
    empresa = Empresa.objects.all().first()  # Suponiendo que solo hay una empresa
    return render(request, 'empresa/empresa.html', {'empresa': empresa})

@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required('empresa.change_empresa', raise_exception=True), name="dispatch")
def editar_empresa(request):
    empresa = Empresa.objects.all().first()  # Suponiendo que solo hay una empresa
    if request.method == 'POST':
        form = EmpresaForm(request.POST, request.FILES, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa actualizada exitosamente.')
            return redirect('empresa:empresa')
        else:
            messages.error(request, 'Error al actualizar la empresa. Por favor, corrige los errores.')
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, 'empresa/editar_empresa.html', {'form': form})

@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required('empresa.delete_empresa', raise_exception=True), name="dispatch")
def eliminar_empresa(request):
    empresa = Empresa.objects.all().first()  # Suponiendo que solo hay una empresa
    if empresa:
        empresa.delete()
        messages.success(request, 'Empresa eliminada exitosamente.')
    else:
        messages.error(request, 'No se encontró la empresa para eliminar.')
    return redirect('empresa:empresa')

@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required('empresa.add_empresa', raise_exception=True), name="dispatch")
def crear_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa creada exitosamente.')
            return redirect('empresa:empresa')
        else:
            messages.error(request, 'Error al crear la empresa. Por favor, corrige los errores.')
    else:
        form = EmpresaForm()
    return render(request, 'empresa/crear_empresa.html', {'form': form})