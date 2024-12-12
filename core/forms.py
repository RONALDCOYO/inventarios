from django import forms
from django.forms import inlineformset_factory
from .models import Cliente, Producto, Factura, DetalleFactura, Abono  

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cedula', 'nombre', 'direccion', 'telefono', 'email']
        widgets = {
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'referencia', 'cantidad', 'ubicacion', 'valor_unitario']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'valor_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['cliente', 'descuento']

DetalleFacturaFormSet = inlineformset_factory(
    Factura, DetalleFactura, fields=['producto', 'cantidad_solicitada', 'valor_unitario'], extra=1, can_delete=True
)

class DetalleFacturaForm(forms.ModelForm):
    class Meta:
        model = DetalleFactura
        fields = ['producto', 'cantidad_solicitada' , 'valor_unitario']

class AbonoForm(forms.ModelForm):
    class Meta:
        model = Abono
        fields = ['factura', 'monto', 'forma_pago']