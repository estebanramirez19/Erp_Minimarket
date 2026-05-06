
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Proveedor
from .forms import ProveedorForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required ,permission_required


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required('proveedor.view_proveedor', raise_exception=True), name="dispatch")
def lista_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, "proveedor/proveedores.html", {"proveedores": proveedores})


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required('proveedor.delete_proveedor', raise_exception=True), name="dispatch")
def eliminar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    proveedor.delete()
    return redirect('proveedor:proveedores')

@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required('proveedor.change_proveedor', raise_exception=True), name="dispatch")
def editar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    formulario = ProveedorForm(request.POST or None, request.FILES or None, instance=proveedor)
    if request.method == "POST" and formulario.is_valid():
        formulario.save()
        return redirect('proveedor:proveedores')
    return render(request, "proveedor/editar_proveedores.html", {"formulario": formulario})

@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required('proveedor.add_proveedor', raise_exception=True), name="dispatch")
def crear_proveedor(request):
    formulario = ProveedorForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and formulario.is_valid():
        formulario.save()
        return redirect('proveedor:proveedores')
    return render(request, "proveedor/crear_proveedores.html", {"formulario": formulario})










