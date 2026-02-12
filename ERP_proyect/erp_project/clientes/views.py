from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Cliente
from .forms import ClienteForm


def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, "clientes/clientes.html", {"clientes": clientes})

def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('cliente:clientes')

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    formulario = ClienteForm(request.POST or None, request.FILES or None, instance=cliente)
    if request.method == "POST" and formulario.is_valid():
        formulario.save()
        return redirect('cliente:clientes')
    return render(request, "clientes/editar_clientes.html", {"formulario": formulario})

def crear_cliente(request):
    formulario = ClienteForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and formulario.is_valid():
        formulario.save()
        return redirect('cliente:clientes')
    return render(request, "clientes/crear_clientes.html", {"formulario": formulario})
