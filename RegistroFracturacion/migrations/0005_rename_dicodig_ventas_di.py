# Generated by Django 4.2.2 on 2023-07-10 02:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RegistroFracturacion', '0004_ventas_dicodig_alter_ventas_cdcomprador'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ventas',
            old_name='dicodig',
            new_name='di',
        ),
    ]
