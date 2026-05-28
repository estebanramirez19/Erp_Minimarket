# account/perms.py
from guardian.shortcuts import assign_perm
from django.contrib.auth.models import Permission
from empresa.models import Empresa


def _add_global_perm(user, codename):
    """Asigna un permiso global (sin objeto) por codename."""
    try:
        perm = Permission.objects.get(codename=codename)
        user.user_permissions.add(perm)
    except Permission.DoesNotExist:
        pass  # Si el permiso no existe aún, no rompe


def asignar_permisos_dueno(user, empresa: Empresa):
    """owner: casi todo, excepto add/delete empresa y add/delete owner."""

    # ── ACCOUNT (custom) ──────────────────────────────────────────────
    _add_global_perm(user, 'can_view_dashboard')
    _add_global_perm(user, 'can_manage_users')
    _add_global_perm(user, 'can_manage_products')
    _add_global_perm(user, 'can_manage_sales')
    _add_global_perm(user, 'can_view_reports')
    _add_global_perm(user, 'add_users')
    _add_global_perm(user, 'edit_users')
    _add_global_perm(user, 'delete_users')
    _add_global_perm(user, 'edit_owner')     # puede editar un dueño

    # ── CLIENTES ──────────────────────────────────────────────────────
    for codename in ['add_cliente', 'change_cliente', 'delete_cliente', 'view_cliente']:
        _add_global_perm(user, codename)

    # ── COMPRAS ───────────────────────────────────────────────────────
    for codename in ['add_compra', 'view_compra']:  # owner no puede editar ni borrar compras
        _add_global_perm(user, codename)

    # ── CONTABILIDAD ──────────────────────────────────────────────────
    for codename in [
        'add_gasto', 'change_gasto', 'delete_gasto', 'view_gasto',
        'add_sistemacaja', 'change_sistemacaja', 'delete_sistemacaja', 'view_sistemacaja',
        'add_inversor', 'change_inversor', 'delete_inversor', 'view_inversor',
        'add_inversion',
    ]:
        _add_global_perm(user, codename)

    # ── EMPRESA (Guardian por objeto) ─────────────────────────────────
    assign_perm('empresa.view_empresa',   user, empresa)
    assign_perm('empresa.change_empresa', user, empresa)  # puede editar
    # ⚠️ owner NO puede add ni delete empresa según tu tabla

    # ── INVENTARIO ────────────────────────────────────────────────────
    for codename in [
        'add_categoriaproducto', 'change_categoriaproducto',
        'delete_categoriaproducto', 'view_categoriaproducto',
        'add_producto', 'change_producto', 'view_producto',
        'add_ajustesinventario', 'change_ajustesinventario',
        'delete_ajustesinventario', 'view_ajustesinventario',
    ]:
        _add_global_perm(user, codename)

    # ── PROVEEDORES ───────────────────────────────────────────────────
    for codename in ['add_proveedor', 'change_proveedor', 'delete_proveedor', 'view_proveedor']:
        _add_global_perm(user, codename)

    # ── VENTAS ────────────────────────────────────────────────────────
    for codename in ['add_venta', 'change_venta', 'view_venta']:  # owner no puede borrar ventas
        _add_global_perm(user, codename)

    user.save()


def asignar_permisos_admin(user, empresa: Empresa):
    """admin: acceso total a todo."""

    # ── ACCOUNT ───────────────────────────────────────────────────────
    for codename in [
        'can_view_dashboard', 'can_manage_users', 'can_manage_products',
        'can_manage_sales', 'can_view_reports',
        'add_users', 'edit_users', 'delete_users',
        'add_owner', 'edit_owner', 'delete_owner',
    ]:
        _add_global_perm(user, codename)

    # ── CLIENTES ──────────────────────────────────────────────────────
    for codename in ['add_cliente', 'change_cliente', 'delete_cliente', 'view_cliente']:
        _add_global_perm(user, codename)

    # ── COMPRAS ───────────────────────────────────────────────────────
    for codename in ['add_compra', 'change_compra', 'delete_compra', 'view_compra']:
        _add_global_perm(user, codename)

    # ── CONTABILIDAD ──────────────────────────────────────────────────
    for codename in [
        'add_gasto', 'change_gasto', 'delete_gasto', 'view_gasto',
        'add_sistemacaja', 'change_sistemacaja', 'delete_sistemacaja', 'view_sistemacaja',
        'add_inversor', 'change_inversor', 'delete_inversor', 'view_inversor',
        'add_inversion',
    ]:
        _add_global_perm(user, codename)

    # ── EMPRESA (Guardian por objeto) ─────────────────────────────────
    assign_perm('empresa.add_empresa',    user, empresa)
    assign_perm('empresa.view_empresa',   user, empresa)
    assign_perm('empresa.change_empresa', user, empresa)
    assign_perm('empresa.delete_empresa', user, empresa)

    # ── INVENTARIO ────────────────────────────────────────────────────
    for codename in [
        'add_categoriaproducto', 'change_categoriaproducto',
        'delete_categoriaproducto', 'view_categoriaproducto',
        'add_producto', 'change_producto', 'delete_producto', 'view_producto',
        'add_ajustesinventario', 'change_ajustesinventario',
        'delete_ajustesinventario', 'view_ajustesinventario',
    ]:
        _add_global_perm(user, codename)

    # ── PROVEEDORES ───────────────────────────────────────────────────
    for codename in ['add_proveedor', 'change_proveedor', 'delete_proveedor', 'view_proveedor']:
        _add_global_perm(user, codename)

    # ── VENTAS ────────────────────────────────────────────────────────
    for codename in ['add_venta', 'change_venta', 'delete_venta', 'view_venta']:
        _add_global_perm(user, codename)

    user.is_staff = True
    user.save()


def asignar_permisos_supervisor(user, empresa: Empresa):
    """supervisor: puede ver y operar, sin borrar cosas importantes."""

    # ── ACCOUNT ───────────────────────────────────────────────────────
    for codename in [
        'can_view_dashboard', 'can_manage_products',
        'can_manage_sales', 'can_view_reports',
        'add_users',
    ]:
        _add_global_perm(user, codename)

    # ── CLIENTES ──────────────────────────────────────────────────────
    for codename in ['add_cliente', 'change_cliente', 'delete_cliente', 'view_cliente']:
        _add_global_perm(user, codename)

    # ── COMPRAS ───────────────────────────────────────────────────────
    for codename in ['add_compra', 'view_compra']:
        _add_global_perm(user, codename)

    # ── CONTABILIDAD ──────────────────────────────────────────────────
    for codename in [
        'add_gasto', 'change_gasto', 'delete_gasto', 'view_gasto',
        'add_sistemacaja', 'change_sistemacaja', 'delete_sistemacaja', 'view_sistemacaja',
    ]:
        _add_global_perm(user, codename)

    # ── EMPRESA (Guardian por objeto) ─────────────────────────────────
    assign_perm('empresa.view_empresa', user, empresa)

    # ── INVENTARIO ────────────────────────────────────────────────────
    for codename in [
        'add_categoriaproducto', 'view_categoriaproducto',
        'add_producto', 'change_producto', 'view_producto',
        'add_ajustesinventario', 'change_ajustesinventario',
        'delete_ajustesinventario', 'view_ajustesinventario',
    ]:
        _add_global_perm(user, codename)

    # ── PROVEEDORES ───────────────────────────────────────────────────
    for codename in ['add_proveedor', 'change_proveedor', 'view_proveedor']:
        _add_global_perm(user, codename)

    # ── VENTAS ────────────────────────────────────────────────────────
    for codename in ['add_venta', 'change_venta', 'view_venta']:
        _add_global_perm(user, codename)

    user.save()


def asignar_permisos_empleado(user, empresa: Empresa):
    """empleado: acceso mínimo, solo operaciones del día a día."""

    # ── ACCOUNT ───────────────────────────────────────────────────────
    _add_global_perm(user, 'can_manage_sales')

    # ── CLIENTES ──────────────────────────────────────────────────────
    _add_global_perm(user, 'add_cliente')

    # ── COMPRAS ───────────────────────────────────────────────────────
    _add_global_perm(user, 'add_compra')

    # ── CONTABILIDAD ──────────────────────────────────────────────────
    for codename in ['add_gasto', 'add_sistemacaja', 'view_sistemacaja']:
        _add_global_perm(user, codename)

    # ── EMPRESA (Guardian por objeto) ─────────────────────────────────
    assign_perm('empresa.view_empresa', user, empresa)

    # ── INVENTARIO ────────────────────────────────────────────────────
    for codename in ['add_producto', 'view_producto']:
        _add_global_perm(user, codename)

    # ── PROVEEDORES ───────────────────────────────────────────────────
    _add_global_perm(user, 'add_proveedor')

    # ── VENTAS ────────────────────────────────────────────────────────
    for codename in ['add_venta', 'view_venta']:
        _add_global_perm(user, codename)

    user.save()