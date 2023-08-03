from django.db import models
from django.contrib.auth.models import Permission

# Create your models here.
class Productos(models.Model):
    codigopr = models.CharField(primary_key=True,max_length=6)
    producto = models.CharField(max_length=50)
    precio = models.PositiveIntegerField()
    cantidad = models.PositiveIntegerField()

class Comprador(models.Model):
    cedula = models.CharField(primary_key=True,max_length=10)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    contratista = models.CharField(max_length=50)

class Factura(models.Model):# tabla temporar
    di = models.AutoField(primary_key=True)
    cdcomprador = models.CharField(max_length=12)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    contratista = models.CharField(max_length=50, blank=True, null=True)
    codigopr = models.CharField(max_length=6)
    producto = models.CharField(max_length=50, blank=True, null=True)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateField()
    precio = models.PositiveIntegerField(blank=True, null=True)
    precioTotal = models.PositiveIntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=300)

class Ventas(models.Model):
    di = models.AutoField(primary_key=True)
    cdcomprador = models.CharField(max_length=12)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    contratista = models.CharField(max_length=50, blank=True, null=True)
    codigopr = models.CharField(max_length=6)
    producto = models.CharField(max_length=50, blank=True, null=True)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateField()
    precio = models.PositiveIntegerField(blank=True, null=True)
    precioTotal = models.PositiveIntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=300)

class Recibo(models.Model):# tabla temporar
    di = models.AutoField(primary_key=True)
    cdcomprador = models.CharField(max_length=12)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    contratista = models.CharField(max_length=50, blank=True, null=True)
    codigopr = models.CharField(max_length=6)
    producto = models.CharField(max_length=50, blank=True, null=True)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateField()
    precio = models.PositiveIntegerField(blank=True, null=True)
    precioTotal = models.PositiveIntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=300)

