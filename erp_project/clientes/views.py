from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Cliente
from .forms import ClienteForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required ,permission_required

@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required('clientes.view_cliente', raise_exception=True), name="dispatch")
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, "clientes/clientes.html", {"clientes": clientes})


@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required('clientes.delete_cliente', raise_exception=True), name="dispatch")
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('cliente:clientes')

@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required('clientes.change_cliente', raise_exception=True), name="dispatch")
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    formulario = ClienteForm(request.POST or None, request.FILES or None, instance=cliente)
    if request.method == "POST" and formulario.is_valid():
        formulario.save()
        return redirect('cliente:clientes')
    return render(request, "clientes/editar_clientes.html", {"formulario": formulario})

@method_decorator(login_required, name="dispatch")
@method_decorator(permission_required('clientes.add_cliente', raise_exception=True), name="dispatch")
def crear_cliente(request):
    formulario = ClienteForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and formulario.is_valid():
        formulario.save()
        return redirect('cliente:clientes')
    return render(request, "clientes/crear_clientes.html", {"formulario": formulario})
