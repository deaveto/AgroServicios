# Generated by Django 4.2.2 on 2023-08-14 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RegistroFracturacion', '0014_recibo_pago'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='pago',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='facturatemp',
            name='pago',
            field=models.BooleanField(default=False),
        ),
    ]