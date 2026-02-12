from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import Venta, DetalleVenta, FolioCounter, Pago  # Descuento
from .forms import VentaForm, DetalleVentaForm  # DescuentoForm
from inventario.models import Producto, Inventario
from django.http import JsonResponse
from django.urls import reverse
from decimal import Decimal, ROUND_HALF_UP


##esto hay que hacerlo pensando en un minimarket real
# Helper para saber si el usuario es administrador/permitido
def es_admin(user):
    return hasattr(user, "perfilusuario") and user.perfilusuario.rol in ['admin', 'dueño', 'gerente']


def crear_venta(request):
    # Crear una venta vacía
    venta = Venta.objects.create(
        subtotal=0,
        iva=0,
        total=0
    )
    # Redirigir al detalle de la nueva venta
    return redirect('ventas:detalle_venta', venta_id=venta.id)



# AGREGAR PRODUCTO MANUALMENTE
def agregar_producto_manual(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == 'POST':
        nombre = request.POST.get('nombre_producto')
        cantidad = int(request.POST.get('cantidad', 1))
        producto = Producto.objects.filter(nombre_producto=nombre).first()
        if producto:
            detalle = DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio_venta
            )
            inventario = Inventario.objects.get(producto=producto)
            inventario.cantidad -= cantidad
            inventario.save()
            messages.success(request, f"{producto.nombre} agregado (x{cantidad}) agregado manualmente.")
            # Si la petición es AJAX, devolver JSON con detalle y totales
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                try:
                    linea_subtotal = float(cantidad) * float(producto.precio_venta)
                except Exception:
                    linea_subtotal = 0.0
                try:
                    TAX_RATE = 0.19
                    venta.subtotal = float(venta.subtotal) + linea_subtotal
                    venta.iva = round(venta.subtotal * TAX_RATE, 2)
                    venta.total = round(venta.subtotal + venta.iva, 2)
                    venta.save()
                except Exception:
                    pass
                return JsonResponse({
                    'success': True,
                    'detalle': {
                        'id': detalle.id,
                        'producto_id': producto.id,
                        'producto_nombre': producto.nombre,
                        'cantidad': cantidad,
                        'precio_unitario': str(producto.precio_venta),
                        'linea_subtotal': f"{linea_subtotal:.2f}",
                    },
                    'totales': {
                        'subtotal': f"{venta.subtotal:.2f}",
                        'iva': f"{venta.iva:.2f}",
                        'total': f"{venta.total:.2f}",
                    }
                })
        else:
            messages.error(request, "Producto no encontrado.")
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Producto no encontrado.'}, status=404)
        return redirect('ventas:detalle_venta', venta_id=venta.id)
    return render(request, 'ventas/agregar_producto_manual.html', {'venta': venta})

# AGREGAR PRODUCTO POR CÓDIGO DE BARRAS
def agregar_producto_por_codigo(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == 'POST':
        codigo = request.POST.get('codigo_barra')
        cantidad = int(request.POST.get('cantidad', 1))
        producto = Producto.objects.filter(codigo_barra=codigo).first()
        if producto:
            detalle = DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio_venta
            )
            inventario = Inventario.objects.get(producto=producto)
            inventario.cantidad -= cantidad
            inventario.save()
            messages.success(request, f"{producto.nombre} agregado (x{cantidad}) por código.")
            # Si la petición es AJAX, devolver JSON con detalle y totales actualizados
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                try:
                    linea_subtotal = float(cantidad) * float(producto.precio_venta)
                except Exception:
                    linea_subtotal = 0.0
                try:
                    TAX_RATE = 0.19
                    venta.subtotal = float(venta.subtotal) + linea_subtotal
                    venta.iva = round(venta.subtotal * TAX_RATE, 2)
                    venta.total = round(venta.subtotal + venta.iva, 2)
                    venta.save()
                except Exception:
                    # ignore calculation errors and return current values
                    pass
                return JsonResponse({
                    'success': True,
                    'detalle': {
                        'id': detalle.id,
                        'producto_id': producto.id,
                        'producto_nombre': producto.nombre,
                        'cantidad': cantidad,
                        'precio_unitario': str(producto.precio_venta),
                        'linea_subtotal': f"{linea_subtotal:.2f}",
                    },
                    'totales': {
                        'subtotal': f"{venta.subtotal:.2f}",
                        'iva': f"{venta.iva:.2f}",
                        'total': f"{venta.total:.2f}",
                    }
                })
        else:
            messages.error(request, "Producto no encontrado.")
        return redirect('ventas:detalle_venta', venta_id=venta.id)
    return render(request, 'ventas/agregar_producto_codigo.html', {'venta': venta})

# QUITAR PRODUCTO DE LA VENTA
def quitar_producto(request, detalle_id):
    detalle = get_object_or_404(DetalleVenta, id=detalle_id)
    venta_id = detalle.venta.id
    # Recuperar inventario si quitas el producto
    inventario = Inventario.objects.get(producto=detalle.producto)
    inventario.cantidad += detalle.cantidad
    inventario.save()
    # Calcular línea subtotal para ajustar totales
    try:
        linea_subtotal = float(detalle.cantidad) * float(detalle.precio_unitario)
    except Exception:
        linea_subtotal = 0.0
    # Borrar detalle
    venta = detalle.venta
    detalle.delete()
    # Ajustar totales de la venta
    try:
        TAX_RATE = 0.19
        venta.subtotal = max(0.0, float(venta.subtotal) - linea_subtotal)
        venta.iva = round(venta.subtotal * TAX_RATE, 2)
        venta.total = round(venta.subtotal + venta.iva, 2)
        venta.save()
    except Exception:
        pass

    # Si la petición es AJAX, devolver JSON con totales actualizados
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'detalle_id': int(detalle_id),
            'totales': {
                'subtotal': f"{venta.subtotal:.2f}",
                'iva': f"{venta.iva:.2f}",
                'total': f"{venta.total:.2f}",
            }
        })

    messages.success(request, "Producto eliminado de la venta.")
    return redirect('ventas:detalle_venta', venta_id=venta_id)

# PRECIO POR PESO
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
@user_passes_test(es_admin)
def historial_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha')
    return render(request, 'ventas/historial_ventas.html', {'ventas': ventas})

# LISTA DE VENTAS (para pantalla principal)
def lista_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha')
    return render(request, 'ventas/lista_ventas.html', {'ventas': ventas})

# DETALLE DE VENTA (pantalla "principal" con productos agregados)
def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = venta.detalles.all()
    productos = Producto.objects.filter(activo=True)
    return render(request, 'ventas/venta.html', {
        'venta': venta,
        'detalles': detalles,
        'productos': productos,
    })

# FINALIZAR VENTA
def finalizar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    
    if request.method == 'POST':
        # Obtener datos del pago del POST
        metodo_pago = request.POST.get('metodo_pago')
        monto_recibido = request.POST.get('monto_recibido', 0)
        tipo_documento_nuevo = request.POST.get('tipo_documento')
        
        # Actualizar tipo de documento si se especifica
        if tipo_documento_nuevo:
            venta.tipo_documento = tipo_documento_nuevo
        
        # Generar folio autoincremental
        folio = FolioCounter.obtener_proximo_folio(venta.tipo_documento)
        
        # Formatear folio según tipo de documento (ej: "BOL-001", "FAC-002")
        prefijos = {
            'Boleta': 'BOL',
            'Factura': 'FAC',
            'Nota de Crédito': 'NC',
            'Nota de Débito': 'ND',
            'Devolución': 'DEV',
            'Sin Documento': 'SD'
        }
        prefijo = prefijos.get(venta.tipo_documento, 'DOC')
        venta.folio = f"{prefijo}-{folio.zfill(6)}"
        venta.save()
        
        # Crear registro de pago
        try:
            monto_recibido = Decimal(str(monto_recibido))
            pago = Pago.objects.create(
                venta=venta,
                metodo=metodo_pago,
                monto_recibido=monto_recibido
            )
            
            # Procesar datos específicos del método de pago
            if metodo_pago == 'Efectivo':
                vuelto = monto_recibido - venta.total
                pago.vuelto = max(Decimal('0'), vuelto)
                pago.save()
            
            elif metodo_pago == 'Tarjeta Débito':
                pago.numero_tarjeta = request.POST.get('numero_tarjeta_debito', '')
                pago.banco = request.POST.get('banco_debito', '')
                pago.save()
            
            elif metodo_pago == 'Tarjeta Crédito':
                pago.numero_tarjeta = request.POST.get('numero_tarjeta_credito', '')
                pago.banco = request.POST.get('banco_credito', '')
                pago.save()
            
            elif metodo_pago == 'Transferencia Bancaria':
                pago.numero_operacion = request.POST.get('numero_operacion', '')
                pago.banco_origen = request.POST.get('banco_origen', '')
                pago.save()
            
            elif metodo_pago == 'Pago Mixto':
                pago.monto_efectivo = Decimal(str(request.POST.get('monto_efectivo', 0)))
                pago.monto_tarjeta = Decimal(str(request.POST.get('monto_tarjeta', 0)))
                pago.monto_transferencia = Decimal(str(request.POST.get('monto_transferencia', 0)))
                pago.numero_tarjeta = request.POST.get('numero_tarjeta_mixto', '')
                pago.numero_operacion = request.POST.get('numero_operacion_mixto', '')
                pago.save()
            
            messages.success(request, f"Venta finalizada. Folio: {venta.folio}")
            
        except Exception as e:
            messages.error(request, f"Error al procesar el pago: {str(e)}")
            return redirect('ventas:detalle_venta', venta_id=venta.id)
        
        # Si la petición es AJAX, devolver JSON con URL para redirigir en cliente
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect_url': reverse('ventas:lista_ventas'), 'folio': venta.folio})
        return redirect('ventas:lista_ventas')
    
    # Si es GET, mostrar formulario de pago
    return render(request, 'ventas/pago.html', {'venta': venta})

# EDITAR VENTA (solo admin)
@user_passes_test(es_admin)
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

# CANCELAR VENTA
def cancelar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == "POST":
        # Recupera al inventario todos los productos vendidos, si lo deseas
        for detalle in venta.detalles.all():
            inventario = Inventario.objects.get(producto=detalle.producto)
            inventario.cantidad += detalle.cantidad
            inventario.save()
        venta.delete()
        messages.success(request, "Venta cancelada.")
        # Si petición AJAX, retornar JSON con redirección
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect_url': reverse('ventas:lista_ventas')})
        return redirect('ventas:lista_ventas')
    return render(request, 'ventas/cancelar_venta.html', {'venta': venta})

# CREAR PROMOCIÓN (solo admin)
@user_passes_test(es_admin)
def crear_promocion(request):
    if request.method == 'POST':
        form = DescuentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Código promocional creado.")
            return redirect('ventas:lista_ventas')
    else:
        form = DescuentoForm()
    return render(request, 'ventas/crear_promocion.html', {'form': form})

# SELECCIONAR MEDIO DE PAGO
def seleccionar_medio_pago(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == 'POST':
        medio = request.POST.get('medio_pago')
        venta.medio_pago = medio
        venta.save()
        messages.success(request, "Medio de pago seleccionado.")
        return redirect('ventas:detalle_venta', venta_id=venta.id)
    return render(request, 'ventas/seleccionar_medio_pago.html', {'venta': venta})

# APLICAR DESCUENTO (stub simple para evitar errores cuando se usa el formulario)
def aplicar_descuento(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == 'POST':
        codigo = (request.POST.get('codigo_descuento') or '').strip()
        TAX_RATE = Decimal('0.19')
        try:
            subtotal = Decimal(str(venta.subtotal))
        except Exception:
            subtotal = Decimal('0.00')

        discount = Decimal('0.00')
        # Soporta códigos simples: PERC-<n> (porcentaje) o FIX-<amount>
        if codigo.upper().startswith('PERC-'):
            try:
                perc = Decimal(codigo.split('-', 1)[1])
                discount = (subtotal * (perc / Decimal('100'))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            except Exception:
                discount = Decimal('0.00')
        elif codigo.upper().startswith('FIX-'):
            try:
                discount = Decimal(codigo.split('-', 1)[1]).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            except Exception:
                discount = Decimal('0.00')
        else:
            # No reconocido: intentar interpretar como porcentaje si es número
            try:
                if codigo:
                    perc = Decimal(codigo)
                    discount = (subtotal * (perc / Decimal('100'))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            except Exception:
                discount = Decimal('0.00')

        subtotal_after = subtotal - discount
        if subtotal_after < Decimal('0.00'):
            subtotal_after = Decimal('0.00')

        iva = (subtotal_after * TAX_RATE).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        total = (subtotal_after + iva).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Persistir cambios
        try:
            venta.subtotal = subtotal_after
            venta.iva = iva
            venta.total = total
            # guardar código si el modelo tiene campo
            try:
                setattr(venta, 'codigo_descuento', codigo)
            except Exception:
                pass
            venta.save()
        except Exception:
            messages.error(request, 'No se pudo aplicar el descuento.')
            return redirect('ventas:detalle_venta', venta_id=venta.id)

        messages.success(request, f"Descuento aplicado: {discount}.")
        # soporte AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'totales': {'subtotal': f"{venta.subtotal:.2f}", 'iva': f"{venta.iva:.2f}", 'total': f"{venta.total:.2f}"}})
        return redirect('ventas:detalle_venta', venta_id=venta.id)
    return redirect('ventas:detalle_venta', venta_id=venta.id)
    return redirect('ventas:detalle_venta', venta_id=venta.id)
