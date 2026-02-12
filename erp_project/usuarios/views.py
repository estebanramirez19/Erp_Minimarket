from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import PerfilUsuario
from .forms import PerfilUsuarioForm



# Listar perfiles de usuario
@login_required
def lista_perfiles(request):
    perfiles = PerfilUsuario.objects.select_related('user').all()
    return render(request, "usuarios/perfiles.html", {"perfiles": perfiles})

# Crear perfil de usuario
@login_required
def crear_perfil(request):
    formulario = PerfilUsuarioForm(request.POST or None)
    if request.method == "POST" and formulario.is_valid():
        perfil = formulario.save(commit=False)
        perfil.user = request.user  # Asignar el usuario actual al perfil
        perfil.save() 
        formulario.save()
        return redirect('usuarios:perfiles')
    else:
        form = PerfilUsuarioForm()
    return render(request, "usuarios/crear_perfil.html", {"formulario": formulario})
    
# Editar perfil
@login_required
def editar_perfil(request, perfil_id):
    perfil = get_object_or_404(PerfilUsuario, id=perfil_id)
    formulario = PerfilUsuarioForm(request.POST or None, instance=perfil)
    if request.method == "POST" and formulario.is_valid():
        formulario.save()
        return redirect('usuarios:perfiles')
    return render(request, "usuarios/editar_perfil.html", {"formulario": formulario})

# Eliminar perfil
@login_required
def eliminar_perfil(request, perfil_id):
    perfil = get_object_or_404(PerfilUsuario, id=perfil_id)
    perfil.delete()
    return redirect('usuarios:perfiles')

