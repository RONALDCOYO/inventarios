# Generated by Django 5.1.4 on 2024-12-11 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_monto_abono_abono_monto_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='abono',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
