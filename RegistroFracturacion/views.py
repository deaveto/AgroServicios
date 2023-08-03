from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from datetime import date
from django.db import IntegrityError
from django.db.models import Sum
from openpyxl import Workbook
from django.http import FileResponse
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
@login_required
def home(request):
    return render(request,"home.html")

@login_required
def ventas(request):
    ListaCliente = Comprador.objects.all()
    ListaContratista = Comprador.objects.all()
    factura = Factura.objects.all()
    context={
        "cliente":ListaCliente,
        "contratista": ListaContratista,
        "ventas": factura
    }
    return render(request,"ventas.html", context)

@login_required
def reporte(request):    
    ListaProductos = Factura.objects.all()
    ListaCliente = Comprador.objects.all()
    ListaProducto = Productos.objects.all()
    context={
        "cliente":ListaCliente,
        "producto":ListaProducto,
        "reporte":ListaProductos,
    }
    return render(request,"reporte.html", context)

@login_required
def inventario(request):
    ListaProductos = Productos.objects.all()
    return render(request,"inventario.html", {"inventario":ListaProductos})    

@login_required
def registrarproducto(request):
    try:
        codigo = request.POST['txtCodigo']
        producto = request.POST['txtProducto']
        precio = request.POST['txtPrecio']
        cantidad = request.POST['txtCantidad']        
        prd = Productos.objects.create(codigopr=codigo,producto=producto, precio=precio,cantidad=cantidad)
        messages.success(request,'¡Productos Registrado!')
        return redirect('/inventario/')
    except IntegrityError:
        messages.success(request,'¡Productos existente!')
        return redirect('/inventario/')
    
#Eliminar producto
@login_required
def eliminacionProducto(request, codigo):
    producto = Productos.objects.get(codigopr=codigo)
    producto.delete()
    messages.success(request,'¡Productos Eliminado!')
    return redirect('/inventario/')

#editar producto
@login_required
def edicionProducto(request, codigo):
    producto = Productos.objects.get(codigopr=codigo)
    return render(request,"edicionProducto.html",{"producto":producto})

@login_required
def editarProducto(request):
    codigo = request.POST['txtCodigo']
    producto = request.POST['txtProducto']
    precio = request.POST['txtPrecio']
    cantidad = request.POST['txtCantidad']
    prd = Productos.objects.get(codigopr=codigo)
    prd.producto = producto
    prd.precio = precio
    prd.cantidad = cantidad
    prd.save()
    messages.success(request,'¡Productos Actualizado!')
    return redirect('/inventario/')

#Registro de compra   
@login_required 
def registrarcompra(request):
    codigoCl = request.POST['Codigo_cliente']
    cliente = Comprador.objects.get(cedula=codigoCl)
    nombre_cliente = cliente.nombre
    apellido_cliente = cliente.apellido
    contratista_cliente = cliente.contratista
    codigoPr = request.POST['Nombre_producto']
    cod = Productos.objects.get(codigopr=codigoPr)
    NomPrd = cod.producto
    cantidad = request.POST['Cant']    
    fecha = date.today()
    prec = Productos.objects.get(codigopr=codigoPr)
    precio = prec.precio
    precioT = int(cantidad) * int(precio)
    descrip = request.POST['desc']        
    prd = Factura.objects.create(cdcomprador=codigoCl,nombre = nombre_cliente,apellido = apellido_cliente, contratista= contratista_cliente, codigopr=codigoPr,producto=NomPrd, cantidad=cantidad,fecha = fecha,precio=precio,precioTotal=precioT, descripcion=descrip)
    messages.success(request,'  ¡Registro de compra OK!')
    return redirect('/reporte/')

# Eliminar compra
@login_required
def eliminacionProductoCompra(request, codigo):
    factura = Factura.objects.get(cdcomprador=codigo)
    factura.delete()
    messages.success(request,'¡Registro Eliminado!')
    return redirect('/reporte/')

# Editar producto
@login_required
def edicionProductoCompra(request, codigo):
    factura = Factura.objects.get(cdcomprador=codigo)
    return render(request,"edicionProductoCompra.html",{"factura":factura})

@login_required
def editarProductoCompra(request):
    codigo = request.POST['txtCodigo']
    codproducto = request.POST['txtProducto']
    cantidad = request.POST['txtCantidad']
    descrip = request.POST['txtDescrip']    
    prd = Factura.objects.get(cdcomprador=codigo)
    Nomprd = Productos.objects.get(codigopr = codproducto)
    prd.codigopr = codproducto
    prd.cantidad = cantidad
    prec = Nomprd.precio
    precioT = int(cantidad) * int(prec)
    prd.precioTotal = precioT
    prd.precio = prec
    prd.producto = Nomprd.producto
    prd.descripcion = descrip
    prd.save()
    messages.success(request,'¡Producto Actualizado!')
    return redirect('/reporte/')

# Copiar los datos temporales en la tabla de ventas
@login_required
def copiarDatosFacturaAventes(request):
    factura = Factura.objects.all()
    for dato in factura:
        venta = Ventas()
        venta.di = dato.di
        venta.cdcomprador = dato.cdcomprador
        venta.nombre = dato.nombre
        venta.apellido = dato.apellido
        venta.contratista = dato.contratista
        venta.codigopr = dato.codigopr
        venta.producto = dato.producto
        venta.cantidad = dato.cantidad
        venta.fecha = dato.fecha
        venta.precio = dato.precio
        venta.precioTotal = dato.precioTotal
        venta.descripcion = dato.descripcion
        venta.save()
        producto = Productos.objects.get(codigopr=dato.codigopr)
        producto.cantidad = int(producto.cantidad)-int(dato.cantidad)
        producto.save()
    factura = Factura.objects.all().delete()
    messages.success(request,'¡Productos Registrados!')
    return redirect('/reporte/')

@login_required
def ConsultaVentasCliente(request):  
    factura = Recibo.objects.all().delete()
    codigoCliente = request.POST['Codigo_cliente']
    fecha_inicio = request.POST['fecha1']
    fecha_fin = request.POST['fecha2']
    datos = Ventas.objects.filter(cdcomprador=codigoCliente, fecha__range=[fecha_inicio, fecha_fin])
    suma_preciototal = datos.aggregate(Sum('precioTotal'))['precioTotal__sum']
    for dato in datos:
        vent = Recibo()
        vent.di = dato.di
        vent.cdcomprador = dato.cdcomprador
        vent.nombre = dato.nombre
        vent.apellido = dato.apellido
        vent.contratista = dato.contratista
        vent.codigopr = dato.codigopr
        vent.producto = dato.producto
        vent.cantidad = dato.cantidad
        vent.fecha = dato.fecha
        vent.precio = dato.precio
        vent.precioTotal = dato.precioTotal
        vent.descripcion = dato.descripcion
        vent.save()
    factura = Recibo.objects.all()
    return render(request, 'ventas.html', {'ventas': factura,'suma_preciototal': suma_preciototal})

@login_required    
def ConsultaVentasContratista(request):    
    factura = Recibo.objects.all().delete()
    contratis = request.POST['Nombre_Contratista']
    fecha_inicio = request.POST['fecha1']
    fecha_fin = request.POST['fecha2']
    venta = Ventas.objects.filter(contratista=contratis, fecha__range=[fecha_inicio, fecha_fin])
    suma_preciototal = venta.aggregate(Sum('precioTotal'))['precioTotal__sum']
    for dato in venta:
        vent = Recibo()
        vent.di = dato.di
        vent.cdcomprador = dato.cdcomprador
        vent.nombre = dato.nombre
        vent.apellido = dato.apellido
        vent.contratista = dato.contratista
        vent.codigopr = dato.codigopr
        vent.producto = dato.producto
        vent.cantidad = dato.cantidad
        vent.fecha = dato.fecha
        vent.precio = dato.precio
        vent.precioTotal = dato.precioTotal
        vent.descripcion = dato.descripcion
        vent.save()
    factura = Recibo.objects.all()
    return render(request, 'ventas.html', {'ventas': factura, 'suma_preciototal': suma_preciototal})

@login_required
def Exportar(request):
    datos =  Recibo.objects.all()
    suma = Recibo.objects.aggregate(total=Sum('precioTotal'))
    total_suma = suma['total'] if suma['total'] else 0
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(['di', 'cdcomprador', 'nombre', 'apellido', 'contratista','fecha', 'codigopr', 'producto', 'cantidad', 'precio','precioTotal','descripcion'])
    # Agrega los datos a las filas
    for dato in datos:
        fila = [dato.di, dato.cdcomprador, dato.nombre, dato.apellido, dato.contratista, dato.fecha, dato.codigopr, dato.producto,  dato.cantidad,  dato.precio, dato.precioTotal, dato.descripcion]  # Reemplaza con los nombres de tus columnas y atributos
        worksheet.append(fila)
    # Crea una respuesta HTTP con el archivo Excel adjunto
    fila = ['-','-','-','-','-','-','-','-','-','Total Suma: ',total_suma]  # Reemplaza con los nombres de tus columnas y atributos
    worksheet.append(fila)   
    excel_file = "datos.xlsx"
    workbook.save(excel_file)
    response = FileResponse(open(excel_file, 'rb'))
    response['Content-Disposition'] = 'attachment; filename=datos.xlsx'  # Nombre del archivo Excel a descargar 
    datos = Recibo.objects.all().delete()
    return response

@login_required    
def LimpiarTablaF(request):
    recibo = Recibo.objects.all()
    recibo.delete()
    messages.success(request,'¡Registro Eliminado!')
    return redirect('/ventas/')

@login_required
def LimpiarTablaR(request):
    factura = Factura.objects.all()
    factura.delete()
    messages.success(request,'¡Registro Eliminado!')
    return redirect('/reporte/')