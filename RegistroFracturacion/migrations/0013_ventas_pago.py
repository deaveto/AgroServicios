# Generated by Django 4.2.2 on 2023-08-12 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RegistroFracturacion', '0012_facturatemp'),
    ]

    operations = [
        migrations.AddField(
            model_name='ventas',
            name='pago',
            field=models.BooleanField(default=False),
        ),
    ]