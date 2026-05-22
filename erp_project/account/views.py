
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from empresa.models import Empresa
from .forms import (
    LoginForm,
    OwnerRegistrationForm,
    SubcuentaForm,
    UserRestrationForm,
)

from .perms import (
    asignar_permisos_dueno,
    asignar_permisos_admin,
    asignar_permisos_supervisor,
    asignar_permisos_empleado,
)

from .models import UserProfile


def user_login(request):
    """Vista de login de usuario."""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Actualizar última conexión
                    if hasattr(user, 'profile'):
                        user.profile.ultima_conexion = user.last_login
                        user.profile.save()
                    messages.success(
                        request, f'Bienvenido {user.first_name or user.username}'
                    )
                    return redirect('inicio')  # o dashboard
                else:
                    messages.error(request, 'Cuenta deshabilitada')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required(login_url='account:login')
def dashboard(request):
    """Inicio del usuario autenticado."""
    return render(request, 'inicio.html', {'user': request.user})


def register_owner(request):
    """
    Registro del dueño de negocio: crea empresa + user + perfil(owner).
    No usar el registro genérico para crear empresas.
    """
    if request.method == 'POST':
        form = OwnerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            empresa = user.profile.empresa
            asignar_permisos_dueno(user, empresa)
            # Logear al dueño recién creado
            login(request, user)
            messages.success(
                request,
                f'Negocio "{user.profile.empresa.razon_social}" registrado.'
            )
            return redirect('inicio')
    else:
        form = OwnerRegistrationForm()
    return render(
        request,
        'account/register_owner.html',
        {'form': form}
    )


@login_required(login_url='account:login')
def crear_subcuenta(request):
    """
    Solo dueño o administrador pueden crear subcuentas dentro de su empresa.
    """
    perfil = request.user.profile
    if perfil.rol not in ['owner', 'administrador','supervisor']:
        messages.error(request, 'No tienes permiso para crear usuarios.')
        return redirect('inicio')

    if request.method == 'POST':
        form = SubcuentaForm(request.POST)
        if form.is_valid():
            rol = form.cleaned_data['rol']
            user = form.save(
                empresa=perfil.empresa,
                rol=form.cleaned_data['rol']
            )
            empresa = perfil.empresa
            if rol == 'administrador':
                asignar_permisos_admin(user, empresa)
            elif rol == 'supervisor':
                asignar_permisos_supervisor(user, empresa)
            elif rol == 'empleado':
                asignar_permisos_empleado(user, empresa)
            messages.success(
                request,
                f'Usuario "{user.username}" creado con rol {user.profile.rol}.'
            )
            return redirect('account:lista_usuarios')
    else:
        form = SubcuentaForm()
    return render(
        request,
        'account/crear_subcuenta.html',
        {'form': form, 'empresa': perfil.empresa}
    )


@login_required(login_url='account:login')
def lista_usuarios(request):
    """
    Lista de usuarios de la misma empresa.
    Solo visible para dueño/admin.
    """
    perfil = request.user.profile
    if not request.user.has_perm('account.view_users'):
        messages.error(request, 'Acceso restringido.')
        return redirect('inicio')

    usuarios = UserProfile.objects.filter(
        empresa=perfil.empresa
    ).select_related('user').order_by('user__first_name')

    return render(
        request,
        'account/lista_usuarios.html',
        {'usuarios': usuarios, 'empresa': perfil.empresa}
    )


@login_required(login_url='account:login')
def user_logout(request):
    """Cierra la sesión del usuario."""
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('inicio')


@login_required(login_url='account:login')
def profile(request):
    """Vista del perfil del usuario."""
    profile = request.user.profile
    return render(request, 'account/profile.html', {'profile': profile})


@login_required(login_url='account:login')
def change_profile(request):
    """Vista para cambiar datos del perfil (en desarrollo)."""
    return HttpResponse("Funcionalidad de cambio de perfil en desarrollo")