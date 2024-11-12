from django.contrib import admin
from .models import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

# Register your models here.
class ListaProductos(admin.ModelAdmin):
    list_display=("codigopr","producto","precio","cantidad")

class ListaComprador(admin.ModelAdmin):
    list_display=("cedula","nombre","apellido","contratista")

class ListaVentas(admin.ModelAdmin):
    list_display=("di","cdcomprador","nombre","apellido","contratista","codigopr","producto","cantidad","fecha","precio","precioTotal","descripcion", "pago")

class ListaContratista(admin.ModelAdmin):
    list_display=("id","nombre")

admin.site.register(Productos, ListaProductos)
admin.site.register(Comprador, ListaComprador)
admin.site.register(Ventas, ListaVentas)
admin.site.register(Recibo, ListaVentas)
admin.site.register(Factura, ListaVentas)
admin.site.register(Contratista,ListaContratista)
admin.site.register(ContentType)
admin.site.register(Permission)