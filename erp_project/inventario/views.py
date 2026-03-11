from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from compras.models import Compra, DetalleCompra, models 

from .models import Producto, Inventario
from .forms import ProductoForm
from .forms import CategoriaProductoForm
from .models import CategoriaProducto
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .models import Inventario, CategoriaProducto


@method_decorator(login_required, name="dispatch")
class InventarioListView(ListView):
    model = Inventario
    template_name = "inventario/productos.html"
    context_object_name = "items"
    paginate_by = 25  # opcional

    def get_queryset(self):
        qs = (
            Inventario.objects
            .select_related("producto", "producto__categoria")
            .order_by("producto__nombre")
        )

        # Búsqueda por nombre o código de barra
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                models.Q(producto__nombre__icontains=q)
                | models.Q(producto__codigo_barra__icontains=q)
            )

        # Filtro por categoría
        categoria_id = self.request.GET.get("categoria")
        if categoria_id:
            qs = qs.filter(producto__categoria_id=categoria_id)

        # Orden por stock
        order = self.request.GET.get("order")
        if order == "stock_asc":
            qs = qs.order_by("cantidad")
        elif order == "stock_desc":
            qs = qs.order_by("-cantidad")

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorias"] = CategoriaProducto.objects.all()
        context["q"] = self.request.GET.get("q", "")
        context["categoria_selected"] = self.request.GET.get("categoria", "")
        context["order"] = self.request.GET.get("order", "")
        return context

def eliminar_producto(request, producto_id): #se queda
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect('inventario:datos_producto')

def editar_producto(request, producto_id): #se queda
    producto = get_object_or_404(Producto, id=producto_id)
    formulario = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if request.method == "POST" and formulario.is_valid():
        formulario.save()
        return redirect('inventario:datos_producto')
    return render(request, "inventario/editar_producto.html", {"formulario": formulario})

def crear_productos(request):  #se queda
    formulario = ProductoForm(request.POST, request.FILES or None)
    if request.method == "POST" and formulario.is_valid():
        formulario.save()
        return redirect('inventario:datos_producto')
    return render(request, "inventario/crear_producto.html", {"formulario": formulario})

def crear_categoria(request): # se queda
    formulario = CategoriaProductoForm(request.POST or None)
    if request.method == "POST" and formulario.is_valid():
        formulario.save()
        return redirect("inventario:crear_producto")  # vuelve al formulario de productos
    return render(request, "inventario/crear_categoria.html", {"formulario": formulario})
