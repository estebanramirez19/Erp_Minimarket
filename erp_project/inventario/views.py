from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Producto, Inventario
from .forms import ProductoForm
from .forms import CategoriaProductoForm
from .models import CategoriaProducto

def datos_producto(request):
    productos = Producto.objects.all().select_related('categoria')
    inventarios = Inventario.objects.all()
    productos_info = []
    for producto in productos:
        inventario = inventarios.filter(producto=producto).first()
        productos_info.append({
            'producto': producto,
            'inventario': inventario,
        })
    contexto = {"productos_info": productos_info}
    return render(request, "inventario/productos.html", contexto)

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect('inventario:datos_producto')

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    formulario = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if request.method == "POST" and formulario.is_valid():
        formulario.save()
        return redirect('inventario:datos_producto')
    return render(request, "inventario/editar_producto.html", {"formulario": formulario})

def crear_producto(request):
    formulario = ProductoForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and formulario.is_valid():
        formulario.save()
        return redirect('inventario:datos_producto')
    return render(request, "inventario/crear_producto.html", {"formulario": formulario})


def crear_categoria(request):
    formulario = CategoriaProductoForm(request.POST or None)
    if request.method == "POST" and formulario.is_valid():
        formulario.save()
        return redirect("inventario:crear_producto")  # vuelve al formulario de productos
    return render(request, "inventario/crear_categoria.html", {"formulario": formulario})
