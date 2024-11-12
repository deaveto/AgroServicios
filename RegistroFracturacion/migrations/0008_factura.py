# Generated by Django 4.2.2 on 2023-07-12 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RegistroFracturacion', '0007_ventas_di_alter_ventas_cdcomprador'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('di', models.AutoField(primary_key=True, serialize=False)),
                ('cdcomprador', models.CharField(max_length=12)),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('apellido', models.CharField(blank=True, max_length=50, null=True)),
                ('contratista', models.CharField(blank=True, max_length=50, null=True)),
                ('codigopr', models.CharField(max_length=6)),
                ('producto', models.CharField(blank=True, max_length=50, null=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('fecha', models.DateField()),
                ('precio', models.PositiveIntegerField(blank=True, null=True)),
                ('precioTotal', models.PositiveIntegerField(blank=True, null=True)),
                ('descripcion', models.CharField(max_length=300)),
            ],
        ),
    ]
