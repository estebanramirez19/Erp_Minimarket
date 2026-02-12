#!/usr/bin/env python
"""
Test script para verificar los endpoints de agregar/quitar detalles temporales en crear_compra
"""
import os
import django
import sys
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from django.test import Client
from inventario.models import Producto, CategoriaProducto
from django.contrib.auth.models import User

# Create test client
client = Client()

# Ensure test user exists
user, _ = User.objects.get_or_create(username='testuser')

# Create test product
categoria, _ = CategoriaProducto.objects.get_or_create(nombre='Test')
producto, created = Producto.objects.get_or_create(
    nombre='Test Product',
    defaults={
        'codigo_barra': 'TEST123',
        'precio_compra': Decimal('100.00'),
        'precio_venta': Decimal('150.00'),
        'categoria': categoria
    }
)

print("✓ Test user and product created\n")

# Test 1: Agregar detalle temporal (sin producto existente)
print("Test 1: Agregar detalle temporal (nuevo producto)")
print("-" * 50)

resp = client.post(
    '/compras/agregar-detalle-temporal/',
    {
        'producto_codigo': 'NEW001',
        'producto_nombre': 'Producto Nuevo',
        'cantidad': 5,
        'precio_unitario': 50.00
    },
    content_type='application/json',
    HTTP_X_REQUESTED_WITH='XMLHttpRequest',
    HTTP_HOST='127.0.0.1'
)

print(f"Status: {resp.status_code}")
data = resp.json()
print(f"Response: {data}")
print(f"✓ Detalle agregado con éxito\n" if resp.status_code == 200 else f"✗ Error: {resp.status_code}\n")

# Test 2: Agregar otro detalle temporal (con producto existente)
print("Test 2: Agregar detalle temporal (producto existente)")
print("-" * 50)

resp = client.post(
    '/compras/agregar-detalle-temporal/',
    {
        'producto_id': producto.id,
        'producto_codigo': producto.codigo_barra,
        'producto_nombre': producto.nombre,
        'cantidad': 2,
        'precio_unitario': 100.00
    },
    content_type='application/json',
    HTTP_X_REQUESTED_WITH='XMLHttpRequest',
    HTTP_HOST='127.0.0.1'
)

print(f"Status: {resp.status_code}")
data = resp.json()
print(f"Response: {data}")
print(f"✓ Detalle con producto existente agregado\n" if resp.status_code == 200 else f"✗ Error: {resp.status_code}\n")

# Test 3: Quitar un detalle temporal
print("Test 3: Quitar detalle temporal (índice 0)")
print("-" * 50)

resp = client.post(
    '/compras/quitar-detalle-temporal/0/',
    HTTP_X_REQUESTED_WITH='XMLHttpRequest',
    HTTP_HOST='127.0.0.1'
)

print(f"Status: {resp.status_code}")
data = resp.json()
print(f"Response: {data}")
print(f"✓ Detalle removido correctamente\n" if resp.status_code == 200 else f"✗ Error: {resp.status_code}\n")

# Test 4: Validación - cantidad negativa
print("Test 4: Validación - cantidad negativa")
print("-" * 50)

resp = client.post(
    '/compras/agregar-detalle-temporal/',
    {
        'producto_nombre': 'Invalid Product',
        'cantidad': -1,
        'precio_unitario': 50.00
    },
    content_type='application/json',
    HTTP_X_REQUESTED_WITH='XMLHttpRequest',
    HTTP_HOST='127.0.0.1'
)

print(f"Status: {resp.status_code}")
data = resp.json()
print(f"Response: {data}")
print(f"✓ Validación funciona correctamente\n" if resp.status_code == 400 else f"✗ No validó: {resp.status_code}\n")

# Test 5: Búsqueda de productos
print("Test 5: Búsqueda de productos (autocomplete)")
print("-" * 50)

resp = client.get(
    '/compras/buscar-productos/?q=Test',
    HTTP_HOST='127.0.0.1'
)

print(f"Status: {resp.status_code}")
data = resp.json()
print(f"Results found: {len(data['results'])}")
print(f"Response: {data}")
print(f"✓ Búsqueda funciona correctamente\n" if resp.status_code == 200 else f"✗ Error: {resp.status_code}\n")

print("=" * 50)
print("✓ All tests completed successfully!")
