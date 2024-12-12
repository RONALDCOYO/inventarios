from decimal import Decimal, InvalidOperation
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import Http404
from .forms import ClienteForm, ProductoForm, DetalleFacturaForm, FacturaForm, AbonoForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Abono, Cliente, Producto, Factura, DetalleFactura
from django.forms import ValidationError, inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})


@login_required
def home_view(request):
    return render(request, 'core/home.html')



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

@login_required
def crear_factura(request):
    productos = Producto.objects.all()  # Obtiene todos los productos
    DetalleFacturaFormSet = inlineformset_factory(Factura, DetalleFactura, form=DetalleFacturaForm, extra=1)
    
    if request.method == 'POST':
        factura_form = FacturaForm(request.POST)
        detalle_formset = DetalleFacturaFormSet(request.POST, request.FILES)
        
        if factura_form.is_valid() and detalle_formset.is_valid():
            factura = factura_form.save(commit=False)
            factura.usuario_creacion = request.user  # Asigna el usuario actual
            factura.save()
            detalles = detalle_formset.save(commit=False)
            for detalle in detalles:
                detalle.factura = factura
                detalle.save()
            return redirect('home')
    else:
        factura_form = FacturaForm()
        detalle_formset = DetalleFacturaFormSet()

    context = {
        'factura_form': factura_form,
        'detalle_formset': detalle_formset,
        'productos': productos,  # Pasa los productos al contexto
    }
    return render(request, 'core/crear_factura.html', context)


def crear_abono(request):
    factura_id = request.GET.get('factura_id')
    factura = get_object_or_404(Factura, id=factura_id)

    if request.method == 'POST':
        try:
            # Obtener el monto del abono desde el formulario y convertirlo a Decimal
            monto_abono = request.POST.get('monto_abono')
            monto_abono = Decimal(monto_abono)

            # Verificar que el monto del abono sea positivo
            if monto_abono <= 0:
                raise ValidationError("El monto del abono debe ser mayor que 0.")

            # Crear el abono
            abono = Abono.objects.create(factura=factura, monto=monto_abono)

            # Actualizar el total de abonos y saldo pendiente de la factura
            factura.total_abonos += monto_abono
            factura.save()  # Esto actualizará el saldo pendiente automáticamente con el nuevo total

            # Redirigir a la página de la factura después de guardar el abono
            return redirect('factura_list')  # Cambia 'factura_list' por la URL correcta si es necesario

        except (ValueError, InvalidOperation) as e:
            # Si el monto del abono no es un número válido
            error_message = "El monto ingresado no es válido."
            return render(request, 'core/crear_abono.html', {'factura': factura, 'error_message': error_message})

        except ValidationError as e:
            # Si el monto del abono es negativo o cero
            return render(request, 'core/crear_abono.html', {'factura': factura, 'error_message': str(e)})

    return render(request, 'core/crear_abono.html', {'factura': factura})



def detalle_abono(request, abono_id):
    abono = get_object_or_404(Abono, id=abono_id)
    return render(request, 'core/detalle_abono.html', {'abono': abono})


def editar_abono(request, abono_id):
    abono = get_object_or_404(Abono, id=abono_id)
    if request.method == 'POST':
        form = AbonoForm(request.POST, instance=abono)
        if form.is_valid():
            form.save()
            return redirect('lista_abonos')  # Redirige a la lista de abonos después de guardar
    else:
        form = AbonoForm(instance=abono)
    return render(request, 'core/editar_abono.html', {'form': form})


def eliminar_abono(request, abono_id):
    abono = get_object_or_404(Abono, id=abono_id)
    abono.delete()
    return redirect('lista_abonos')  # Redirige a la lista de abonos después de eliminar



def lista_abonos(request):
    abonos = Abono.objects.all()
    return render(request, 'core/lista_abonos.html', {'abonos': abonos})


def factura_detalle(request, factura_id):
    factura = Factura.objects.get(id=factura_id)
    return render(request, 'core/factura_detalle.html', {'factura': factura})



def factura_list(request):
    # Obtener todas las facturas
    facturas = Factura.objects.all()

    # Calcular el total de abonos realizados a cada factura
    for factura in facturas:
        # Obtener los abonos realizados a esta factura
        abonos = Abono.objects.filter(factura=factura)
        
        # Calcular el total de abonos realizados
        total_abonos = abonos.aggregate(Sum('monto'))['monto__sum'] or 0
        
        # Calcular el saldo pendiente de la factura
        saldo_pendiente = factura.total - total_abonos  # Calcular el saldo pendiente directamente
        
        # Asignar el total de abonos calculado
        factura.total_abonos = total_abonos
        
        # No necesitas asignar saldo_pendiente, ya que es una propiedad calculada automáticamente

    return render(request, 'factura_list.html', {'facturas': facturas})