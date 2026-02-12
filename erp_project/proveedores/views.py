
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Proveedor
from .forms import ProveedorForm

def lista_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, "proveedor/proveedores.html", {"proveedores": proveedores})


def eliminar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    proveedor.delete()
    return redirect('proveedor:proveedores')

def editar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    formulario = ProveedorForm(request.POST or None, request.FILES or None, instance=proveedor)
    if request.method == "POST" and formulario.is_valid():
        formulario.save()
        return redirect('proveedor:proveedores')
    return render(request, "proveedor/editar_proveedores.html", {"formulario": formulario})

def crear_proveedor(request):
    formulario = ProveedorForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and formulario.is_valid():
        formulario.save()
        return redirect('proveedor:proveedores')
    return render(request, "proveedor/crear_proveedores.html", {"formulario": formulario})










