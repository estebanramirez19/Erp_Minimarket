from decimal import Decimal

from django import db
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction, models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from inventario.models import Producto
from proveedores.models import Proveedor

from .forms import CompraForm, DetalleCompraFormSet
from .models import Compra, DetalleCompra


# === BÚSQUEDA AJAX DE PRODUCTOS ===
@login_required
def buscar_productos(request):
    q = request.GET.get("q", "").strip()
    results = []

    if q:
        qs = (
            Producto.objects.filter(
                models.Q(nombre__icontains=q)
                | models.Q(codigo_barra__icontains=q)
            )
            .select_related()[:15]
        )

        for p in qs:
            results.append(
                {
                    "id": p.id,
                    "nombre": p.nombre,
                    "codigo_barra": getattr(p, "codigo_barra", ""),
                    "precio_compra": (
                        f"{p.precio_compra:.2f}"
                        if getattr(p, "precio_compra", None) is not None
                        else "0.00"
                    ),
                }
            )

    return JsonResponse({"results": results})


# === CREAR COMPRA + DETALLES ===
@login_required
@transaction.atomic
def compra_crear(request):
    if request.method == "POST":
        compra_form = CompraForm(request.POST, request.FILES)
        formset = DetalleCompraFormSet(request.POST, prefix="detalles")

        if compra_form.is_valid() and formset.is_valid():
            compra = compra_form.save(commit=False)
            compra.usuario = request.user

            # Cargar snapshot del proveedor
            if compra.proveedor_id:
                p = compra.proveedor
                compra.razon_social_proveedor = getattr(p, "razon_social", "")
                compra.rut_proveedor = getattr(p, "rut", "")
                compra.giro_proveedor = getattr(p, "giro", "")
                compra.direccion_proveedor = getattr(p, "direccion", "")
                compra.email_proveedor = getattr(p, "email", "")
                compra.comuna_proveedor = getattr(p, "comuna", "")
                compra.ciudad_proveedor = getattr(p, "ciudad", "")

            compra.save()

            formset.instance = compra
            formset.save()

            compra.calcular_totales()

            messages.success(request, "Compra registrada correctamente.")
            return redirect("compras:detalle", compra_id=compra.pk)
    else:
        compra_form = CompraForm()
        formset = DetalleCompraFormSet(prefix="detalles")

    context = {
        "compra_form": compra_form,
        "formset": formset,
    }
    return render(request, "compras/compra_form.html", context)


# === LISTA DE COMPRAS ===
@login_required
def lista_compras(request):
    compras = Compra.objects.all().order_by("-fecha_compra", "-id")
    return render(
        request,
        "compras/lista_compras.html",
        {"compras": compras},
    )


# === DETALLE DE COMPRA ===
@login_required
def detalle_compra(request, compra_id):
    compra = get_object_or_404(
        Compra.objects.select_related("proveedor", "usuario"),
        id=compra_id,
    )
    detalles = (
        compra.detalles.select_related("producto")
        .all()
        .order_by("id")
    )

    return render(
        request,
        "compras/detalle_compra.html",
        {
            "compra": compra,
            "detalles": detalles,
        },
    )


# === EDITAR COMPRA (placeholder para implementar luego) ===
@login_required
@transaction.atomic
def editar_compra(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)

    if request.method == "POST":
        compra_form = CompraForm(request.POST, request.FILES, instance=compra)
        formset = DetalleCompraFormSet(
            request.POST,
            prefix="detalles",
            instance=compra,
        )

        if compra_form.is_valid() and formset.is_valid():
            compra = compra_form.save(commit=False)

            # Si cambias el proveedor, puedes actualizar el snapshot si quieres
            if compra.proveedor_id:
                p = compra.proveedor
                compra.razon_social_proveedor = getattr(p, "razon_social", "")
                compra.rut_proveedor = getattr(p, "rut", "")
                compra.giro_proveedor = getattr(p, "giro", "")
                compra.direccion_proveedor = getattr(p, "direccion", "")
                compra.email_proveedor = getattr(p, "email", "")
                compra.comuna_proveedor = getattr(p, "comuna", "")
                compra.ciudad_proveedor = getattr(p, "ciudad", "")

            compra.save()
            formset.save()
            compra.calcular_totales()

            messages.success(request, "Compra actualizada correctamente.")
            return redirect("compras:detalle", compra_id=compra.pk)
    else:
        compra_form = CompraForm(instance=compra)
        formset = DetalleCompraFormSet(prefix="detalles", instance=compra)

    return render(
        request,
        "compras/compra_form.html",
        {
            "compra_form": compra_form,
            "formset": formset,
            "compra": compra,
            "modo_edicion": True,
        },
    )


# === ELIMINAR COMPRA ===
@login_required
@transaction.atomic
def eliminar_compra(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)

    if request.method == "POST":
        compra.delete()
        messages.success(request, "Compra eliminada correctamente.")
        return redirect("compras:lista_compras")

    return render(
        request,
        "compras/eliminar_compra.html",
        {"compra": compra},
    )
