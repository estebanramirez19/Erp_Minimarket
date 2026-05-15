from guardian.shortcuts import assign_perm
from empresa.models import Empresa


def asignar_permisos_dueno(user, empresa: Empresa):
    """
    Da permisos de objeto sobre una empresa al dueño.
    """
    # Permisos típicos de empresa
    assign_perm('empresa.view_empresa', user, empresa)
    assign_perm('empresa.change_empresa', user, empresa)
    assign_perm('empresa.delete_empresa', user, empresa)
    assign_perm('empresa.add_empresa', user, empresa)


def asignar_permisos_admin(user, empresa: Empresa):
    """
    Admin de empresa: puede ver y editar, pero no borrar.
    """
    assign_perm('empresa.view_empresa', user, empresa)
    assign_perm('empresa.change_empresa', user, empresa)


def asignar_permisos_empleado(user, empresa: Empresa):
    """
    Empleado: solo puede ver info básica de la empresa (si quieres).
    """
    assign_perm('empresa.view_empresa', user, empresa)