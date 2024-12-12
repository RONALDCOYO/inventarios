from django.db import IntegrityError, models
from django.contrib.auth.models import User

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
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    numero_factura = models.CharField(max_length=20, unique=True, blank=True, null=True)
    total_abonos = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Este campo es el que utilizamos para acumular los abonos

    @property
    def total(self):
        # Calcula el total sumando los precios de los detalles de la factura
        total_items = sum(item.valor_total for item in self.detalles.all())
        total_con_descuento = total_items - self.descuento if self.descuento else total_items
        return total_con_descuento

    @property
    def saldo_pendiente(self):
        # Calcula el saldo pendiente de la factura (total - total de abonos)
        return self.total - self.total_abonos

    def save(self, *args, **kwargs):
        if not self.numero_factura:
            self.numero_factura = self.generar_numero_factura()
        max_retries = 5
        for attempt in range(max_retries):
            try:
                super(Factura, self).save(*args, **kwargs)
                break
            except IntegrityError:
                if attempt < max_retries - 1:
                    self.numero_factura = self.generar_numero_factura()
                else:
                    raise

    def generar_numero_factura(self):
        ultimo_registro = Factura.objects.all().order_by('id').last()
        if not ultimo_registro or not ultimo_registro.numero_factura:
            nuevo_numero = 1
        else:
            nuevo_numero = int(ultimo_registro.numero_factura.split('-')[-1]) + 1
        return f"FAC-{nuevo_numero:05d}"

    
class DetalleFactura(models.Model):
    factura = models.ForeignKey('Factura', related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad_solicitada = models.PositiveIntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Descontar del inventario
        self.producto.cantidad -= self.cantidad_solicitada
        self.producto.save()
        # Calcular el valor total
        self.valor_total = self.cantidad_solicitada * self.valor_unitario
        super().save(*args, **kwargs)
        
class Abono(models.Model): 
    factura = models.ForeignKey(Factura, related_name='abonos', on_delete=models.CASCADE)
    fecha_abono = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pago = models.CharField(
        max_length=50, 
        choices=[
            ('contado', 'Contado'),
            ('credito', 'Crédito'),
            ('cheque', 'Cheque'),
            ('consignacion', 'Consignación'),
            ('transferencia', 'Transferencia'),
            ('efectivo', 'Efectivo'),
        ],
        default='efectivo'  # Valor predeterminado
    )
    saldo_pendiente = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Actualizar el saldo pendiente
        self.saldo_pendiente = self.factura.total - sum(abono.monto for abono in self.factura.abonos.all()) - self.monto
        super().save(*args, **kwargs)