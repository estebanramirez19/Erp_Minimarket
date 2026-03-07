from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Venta, DetalleVenta, FolioCounter, Pago  # Descuento
from .forms import DetalleVentaFormSet, VentaForm, DetalleVentaForm  # DescuentoForm
from inventario.models import Producto, Inventario
from django.http import JsonResponse
from django.urls import reverse
from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction, models


#Solo hare a view de crear venta pero bien hecha

@login_required
@transaction.atomic
def crear_venta(request): # recibe los fomularios de venta y detalle 
    if request.method == 'POST':
        venta_form = VentaForm(request.POST, request.FILES)
        formset = DetalleVentaFormSet(request.POST, prefix='detalle venta')
        #creo que falta agregar el metodo de pago

        if venta_form.is_valid() and formset.is_valid():
            venta = venta_form.save(commit=False)
            venta.usuario = request.user

            venta.empresa_razonsocial = request.user.profile.empresa.razonsocial
            venta.empresa_rut = request.user.profile.empresa.rut
            venta.empresa_giro = request.user.profile.empresa.giro
            venta.empresa_direccion = request.user.profile.empresa.direccion
            venta.empresa_comuna = request.user.profile.empresa.comuna
            venta.empresa_ciudad = request.user.profile.empresa.ciudad

            if venta.cliente_id:
                venta.nombre_cliente = venta.cliente.nombre
                venta.rut_cliente = venta.cliente.rut

            venta.save()
            formset.instance = venta
            formset.save()

            venta.calcular_totales()  

            messages.success(request, "Venta creada exitosamente.")
    else:
        venta_form = VentaForm()
        formset = DetalleVentaFormSet(prefix='detalle venta')
    
    context = {
        'venta_form': venta_form,
        'formset': formset,
    }
    return render(request, 'ventas/crear_venta.html', context)


 #preCIO POR PESO
def precio_por_peso(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        peso = float(request.POST.get('peso'))
        producto = Producto.objects.get(id=producto_id)
        DetalleVenta.objects.create(
            venta=venta,
            producto=producto,
            cantidad=peso,
            precio_unitario=producto.precio_venta
        )
        inventario = Inventario.objects.get(producto=producto)
        inventario.cantidad -= peso
        inventario.save()
        messages.success(request, f"Producto {producto.nombre} agregado por peso ({peso}kg).")
        return redirect('ventas:detalle_venta', venta_id=venta.id)
    productos = Producto.objects.filter(activo=True)
    return render(request, 'ventas/precio_por_peso.html', {'venta': venta, 'productos': productos})

# HISTORIAL DE VENTAS (solo admin)
@login_required
def historial_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha')
    return render(request, 'ventas/historial_ventas.html', {'ventas': ventas})

# LISTA DE VENTAS (para pantalla principal)
def lista_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha')
    return render(request, 'ventas/lista_ventas.html', {'ventas': ventas})

# EDITAR VENTA (solo admin)
@login_required
def editar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            messages.success(request, "Venta actualizada correctamente.")
            return redirect('ventas:historial_ventas')
    else:
        form = VentaForm(instance=venta)
    return render(request, 'ventas/editar_venta.html', {'form': form, 'venta': venta})


