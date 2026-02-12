# integrations/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Producto, LecturaCodigo

@csrf_exempt
def lector_codigo(request):
    if request.method == "POST":
        codigo = request.POST.get('codigo')
        producto = Producto.objects.filter(codigo_barra=codigo).first()
        if producto:
            LecturaCodigo.objects.create(producto=producto, codigo=codigo, usuario=request.user if request.user.is_authenticated else None)
            return JsonResponse({
                "success": True,
                "producto": {
                    "id": producto.id,
                    "nombre": producto.nombre,
                    "precio_venta": float(producto.precio_venta),
                    "codigo_barra": producto.codigo_barra,
                }
            })
        else:
            return JsonResponse({"success": False, "error": "Producto no encontrado"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)

