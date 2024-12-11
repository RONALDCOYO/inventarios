from django.shortcuts import render, redirect
from .forms import ClienteForm, ProductoForm
from .models import Cliente, Producto

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes_listar')  # Redirige a la lista de clientes
    else:
        form = ClienteForm()
    return render(request, 'core/crear_cliente.html', {'form': form})

def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'core/listar_clientes.html', {'clientes': clientes})

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos_listar')  # Redirige a la lista de productos
    else:
        form = ProductoForm()
    return render(request, 'core/crear_producto.html', {'form': form})

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'core/listar_productos.html', {'productos': productos})
