#!/usr/bin/env python
"""
End-to-end test: Upload PDF to procesar-pdf, add extracted products to session via batch endpoint,
then GET crear_compra page and verify session has 'compra_detalles_temp'.
"""
import os
import sys
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
django.setup()

from django.test import Client

PDF_PATH = r"c:\Users\esteb\Desktop\factura_prueba.pdf"

client = Client()

print('Uploading PDF to /compras/procesar-pdf/')
with open(PDF_PATH, 'rb') as f:
    # set HTTP_HOST to avoid DisallowedHost in test client
    response = client.post('/compras/procesar-pdf/', {'pdf': f}, follow=True, HTTP_HOST='localhost')

print('Status:', response.status_code)
try:
    data = response.json()
except Exception:
    print('Response content not JSON:')
    print(response.content[:1000])
    sys.exit(1)

print('Response JSON keys:', list(data.keys()))
if not data.get('success'):
    print('Processing failed:', data)
    sys.exit(1)

print('PDF processed. Extracted products count:', len(data.get('productos', [])))
products = data.get('productos', [])
# Prepare items for batch endpoint; map fields
items = []
for p in products:
    items.append({
        'producto_id': p.get('producto_id') if p.get('producto_id') else None,
        'producto_codigo': p.get('producto_codigo', ''),
        'producto_codigo_proveedor': '',
        'producto_nombre': p.get('producto_nombre') or p.get('nombre') or '',
        'cantidad': p.get('cantidad') or 1,
        'precio_unitario': p.get('precio_unitario') or p.get('precio') or 0
    })

print('Posting', len(items), 'items to /compras/agregar-detalles-temporales-batch/')
# Use HTTP_HOST to avoid DisallowedHost during tests
response2 = client.post('/compras/agregar-detalles-temporales-batch/', json.dumps({'items': items}), content_type='application/json', HTTP_HOST='localhost')
print('Batch status:', response2.status_code)
try:
    j2 = response2.json()
    print('Batch response:', json.dumps(j2, indent=2))
except Exception:
    print('Batch response content:', response2.content[:1000])
    sys.exit(1)

# Now GET crear_compra to inspect context/session
print('Fetching crear_compra page...')
resp3 = client.get('/compras/crear-compra/', HTTP_HOST='localhost')
print('crear_compra status:', resp3.status_code)
# Try to access session directly
session = client.session
detalles = session.get('compra_detalles_temp', [])
print('Session compra_detalles_temp count:', len(detalles))
for d in detalles:
    print('-', d.get('producto_nombre'), 'qty:', d.get('cantidad'), 'price:', d.get('precio_unitario'))

print('Done.')
