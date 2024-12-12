# Generated by Django 5.1.4 on 2024-12-11 19:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='abono',
            old_name='monto_abono',
            new_name='monto',
        ),
        migrations.RemoveField(
            model_name='abono',
            name='metodo_pago',
        ),
        migrations.RemoveField(
            model_name='factura',
            name='numero_factura',
        ),
        migrations.AddField(
            model_name='abono',
            name='forma_pago',
            field=models.CharField(choices=[('contado', 'Contado'), ('credito', 'Crédito'), ('cheque', 'Cheque'), ('consignacion', 'Consignación'), ('transferencia', 'Transferencia'), ('efectivo', 'Efectivo')], default='efectivo', max_length=50),
        ),
        migrations.AddField(
            model_name='abono',
            name='saldo_pendiente',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='factura',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='abono',
            name='factura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='abonos', to='core.factura'),
        ),
        migrations.AlterField(
            model_name='factura',
            name='descuento',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='factura',
            name='usuario_creacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='DetalleFactura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_solicitada', models.PositiveIntegerField()),
                ('valor_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='core.factura')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.producto')),
            ],
        ),
        migrations.DeleteModel(
            name='ReciboDeCaja',
        ),
    ]