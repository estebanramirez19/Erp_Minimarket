from django.shortcuts import render
from inventario.models import Producto, Inventario
from clientes.models import Cliente
from proveedores.models import Proveedor
from ventas.models import Venta
from compras.models import Compra
from usuarios.models import PerfilUsuario
from django.db.models import Sum
from decimal import Decimal

def inicio(request):
    # Estadísticas generales
    total_productos = Producto.objects.count()
    total_clientes = Cliente.objects.count()
    total_proveedores = Proveedor.objects.count()
    total_ventas = Venta.objects.count()
    total_compras = Compra.objects.count()
    total_usuarios = PerfilUsuario.objects.count()
    
    # Totales financieros
    ventas_total = Venta.objects.aggregate(Sum('total'))['total__sum'] or Decimal('0.00')
    compras_total = Compra.objects.aggregate(Sum('total'))['total__sum'] or Decimal('0.00')
    
    # Stock total en inventario
    stock_items = Inventario.objects.aggregate(Sum('cantidad'))['cantidad__sum'] or 0
    
    # Productos con stock bajo (< 10)
    productos_stock_bajo = Producto.objects.filter(
        inventario__cantidad__lt=10, 
        activo=True
    ).count()
    
    contexto = {
        "total_productos": total_productos,
        "total_clientes": total_clientes,
        "total_proveedores": total_proveedores,
        "total_ventas": total_ventas,
        "total_compras": total_compras,
        "total_usuarios": total_usuarios,
        "ventas_total": f"{ventas_total:.2f}",
        "compras_total": f"{compras_total:.2f}",
        "stock_items": stock_items,
        "productos_stock_bajo": productos_stock_bajo,
    }
    return render(request, "inicio.html", contexto)
