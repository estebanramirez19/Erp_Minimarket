from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db import models
from proveedores.models import Proveedor
from inventario.models import Producto
from .models import Compra, DetalleCompra
from .forms import CompraForm, DetalleCompraFormSet
from decimal import Decimal


def buscar_productos(request):
    q = request.GET.get('q', '').strip()
    results = []
    if q:
        qs = Producto.objects.filter(models.Q(nombre__icontains=q) | models.Q(codigo_barra__icontains=q))[:15]
        for p in qs:
            results.append({
                'id': p.id,
                'nombre': p.nombre,
                'codigo_barra': getattr(p, 'codigo_barra', ''),
                'precio_compra': f"{p.precio_compra:.2f}" if getattr(p, 'precio_compra', None) is not None else '0.00'
            })
    return JsonResponse({'results': results})




# === LISTA DE COMPRAS ===
def lista_compras(request):
    compras = Compra.objects.all().order_by('-fecha')
    return render(request, 'compras/lista_compras.html', {'compras': compras})

# === CREAR COMPRA MANUAL O CON PDF OCR ===
def crear_compra(request):
    pass



# === DETALLE DE COMPRA (ver productos incluidos en la compra) ===
##aca es donde debo ingresar los productos llamando a inventario para tener todo eso 
def detalle_compra(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    detalles = compra.detalles.all()
    productos = Producto.objects.all()
    return render(request, 'compras/detalle_compra.html', {
        'compra': compra,
        'detalles': detalles,
        'productos': productos,
    })



# === EDITAR COMPRA ===
def editar_compra(request, compra_id):
    pass




# === ELIMINAR COMPRA ===
def eliminar_compra(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    if request.method == "POST":
        compra.delete()
        messages.success(request, "Compra eliminada correctamente.")
        return redirect('compras:lista_compras')
    return render(request, 'compras/eliminar_compra.html', {'compra': compra})
