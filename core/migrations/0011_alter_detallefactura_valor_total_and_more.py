# Generated by Django 5.1.4 on 2024-12-18 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_abono_saldo_pendiente_factura_total_abonos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallefactura',
            name='valor_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='cantidad',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
