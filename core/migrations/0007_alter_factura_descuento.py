# Generated by Django 5.1.4 on 2024-12-12 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_factura_numero_factura'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='descuento',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]