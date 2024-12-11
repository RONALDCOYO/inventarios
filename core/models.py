from django.db import models

class Cliente(models.Model):
    cedula = models.CharField(max_length=15, unique=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    referencia = models.CharField(max_length=50, unique=True)
    cantidad = models.PositiveIntegerField()
    ubicacion = models.CharField(max_length=255)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    usuario_creacion = models.CharField(max_length=100)  # Nombre del usuario que crea la factura
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    numero_factura = models.CharField(max_length=20, unique=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.numero_factura

class Abono(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    monto_abono = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_abono = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=50)  # Contado, cheque, transferencia, etc.

    def __str__(self):
        return f'Abono de {self.monto_abono} a {self.factura.numero_factura}'

class ReciboDeCaja(models.Model):
    abono = models.OneToOneField(Abono, on_delete=models.CASCADE)
    recibo_numero = models.CharField(max_length=20, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Recibo {self.recibo_numero} para factura {self.abono.factura.numero_factura}'
