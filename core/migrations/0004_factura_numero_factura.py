# Generated by Django 5.1.4 on 2024-12-11 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_factura_abono'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='numero_factura',
            field=models.CharField(default=0, max_length=20, unique=True),
            preserve_default=False,
        ),
    ]