from django.shortcuts import render, redirect
from .forms import LoginForm, UserRestrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User


def user_login(request):
    """Vista de login de usuario"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, 
                                username=cd['username'], 
                                password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Bienvenido {user.first_name or user.username}')
                    return redirect('inicio')
                else:
                    messages.error(request, 'Cuenta deshabilitada')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    
    return render(request, 'account/login.html', {'form': form})


@login_required(login_url='account:login')
def dashboard(request):
    """Dashboard del usuario autenticado"""
    return render(request, 'account/dashboard.html', {'user': request.user})


def register(request):
    """Vista de registro de nuevo usuario"""
    if request.method == 'POST':
        user_form = UserRestrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            password = user_form.cleaned_data['password']
            new_user.set_password(password)
            new_user.save()
            messages.success(request, 'Usuario registrado exitosamente. Inicia sesión.')
            return redirect('account:login')
        else:
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        user_form = UserRestrationForm()
    
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required(login_url='account:login')
def user_logout(request):
    """Cierra la sesión del usuario"""
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('inicio')


@login_required(login_url='account:login')
def profile(request):
    """Vista del perfil del usuario"""
    profile = request.user.profile
    return render(request, 'account/profile.html', {'profile': profile})