import os
import django
import json

# Ensure project root is on sys.path so 'erp_project' package is importable
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from django.contrib.auth.models import User
from proveedores.models import Proveedor
from inventario.models import CategoriaProducto, Producto
from compras.models import Compra, DetalleCompra
from django.test import Client

print('Iniciando script de prueba de compras (AJAX)')

# Usuario
user = User.objects.first()
if not user:
    print('Creando usuario de prueba')
    user = User.objects.create_user('testuser', 'test@example.com', 'testpass')

# Proveedor
prov = Proveedor.objects.first()
if not prov:
    print('Creando proveedor de prueba')
    prov = Proveedor.objects.create(nombre='Prov Test', contacto='Contacto', direccion='Direccion 1', email='prov@test.com', telefono='123456789')

# Categoria y Producto
cat = CategoriaProducto.objects.first()
if not cat:
    cat = CategoriaProducto.objects.create(nombre='Categoria Test')

prod = Producto.objects.first()
if not prod:
    print('Creando producto de prueba')
    prod = Producto.objects.create(
        nombre='Producto Test',
        descripcion='Desc',
        codigo_barra='TEST12345',
        categoria=cat,
        precio_venta=10.00,
        precio_compra=8.00,
        activo=True
    )

# Compra
compra = Compra.objects.first()
if not compra:
    print('Creando compra de prueba')
    compra = Compra.objects.create(proveedor=prov, usuario=user, tipo_documento='Factura')

print(f'Usando Compra id={compra.id}, Producto id={prod.id}')

client = Client()

# agregar detalle
url_agregar = f"/compras/{compra.id}/agregar-detalle/"
post_data = {'producto_id': str(prod.id), 'cantidad': '3', 'precio_unitario': '12.50'}
print('POST', url_agregar, post_data)
resp = client.post(url_agregar, post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest', HTTP_HOST='127.0.0.1')
print('Status:', resp.status_code)
ct = resp.content.decode(errors='replace')
print('Response length:', len(ct))
print('Response preview (first 1000 chars):')
print(ct[:1000])

# Obtener ultimo detalle
ultimo = compra.detalles.order_by('-id').first()
if ultimo:
    print('Detalle creado id=', ultimo.id)
    url_quitar = f"/compras/detalle/{ultimo.id}/quitar/"
    print('POST', url_quitar)
    resp2 = client.post(url_quitar, {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest', HTTP_HOST='127.0.0.1')
    print('Status:', resp2.status_code)
    try:
        print('JSON:', json.loads(resp2.content.decode()))
    except Exception:
        print('Resp text:', resp2.content.decode())
else:
    print('No se creó detalle, abortando test de eliminación')

print('Script finalizado')
