from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from datetime import date
from django.db import IntegrityError
from django.db.models import Sum
from openpyxl import Workbook
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render


#Crea decoradores de vista personalizados que verificarán los permisos de los usuarios
def es_administrador(user):
    result = user.groups.filter(name='Administrador').exists()
    print(f"Usuario {user} es administrador: {result}")
    return result
def es_gestor(user):
    result = user.groups.filter(name='Gestor').exists()
    print(f"Usuario {user} es gestor: {result}")
    return result
def es_administrador_o_gestor(user):
    return user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Gestor').exists()
def no_tiene_permisos(request):
    return render(request, 'no_permisos.html') 



# Create your views here.
@login_required #funcion para que deba de iniciar sesión antes de ongresar a las vistas
def home(request):
    return render(request,"home.html")

def home1(request):
    return render(request,"base1.html")

@login_required #funcion para que deba de iniciar sesión antes de ongresar a las vistas
@user_passes_test(es_administrador_o_gestor)
def inventario(request):
    ListaProductos = Productos.objects.all()               
    return render(request,"inventario.html", {"inventario":ListaProductos}) 

@login_required #funcion para que deba de iniciar sesión antes de ongresar a las vistas
@user_passes_test(es_administrador_o_gestor)
def ventas(request):
    ListaCliente = Comprador.objects.all()
    ListaContratista = Contratista.objects.all()
    factura = Recibo.objects.all()
   
    context={
        "cliente":ListaCliente,
        "contratista": ListaContratista,
        "ventas": factura
    }
    return render(request,"ventas.html", context)
     
@login_required #funcion para que deba de iniciar sesión antes de ongresar a las vistas
@user_passes_test(es_administrador, no_tiene_permisos)
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
@login_required #funcion para que deba de iniciar sesión antes de ongresar a las vistas
@user_passes_test(es_administrador,no_tiene_permisos)
def eliminacionProducto(request, codigo):
    producto = Productos.objects.get(codigopr=codigo)
    producto.delete()
    messages.success(request,'¡Productos Eliminado!')
    return redirect('/inventario/')

#editar producto
@login_required #funcion para que deba de iniciar sesión antes de ongresar a las vistas
@user_passes_test(es_administrador, no_tiene_permisos)
def edicionProducto(request, codigo):
    producto = Productos.objects.get(codigopr=codigo)
    return render(request,"edicionProducto.html",{"producto":producto})

@login_required #funcion para que deba de iniciar sesión antes de ongresar a las vistas
@user_passes_test(es_administrador, no_tiene_permisos)
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
# factura_agregados = [] 
@login_required #funcion para que deba de iniciar sesión antes de ongresar a las vistas
@user_passes_test(es_administrador_o_gestor)

def reporte(request):   
    #ListaProductos = factura_agregados 
    ListaProductos = Factura.objects.all()
    ListaCliente = Comprador.objects.all()
    ListaProducto = Productos.objects.all()

    # Obtener todas las facturas
    facturas = Factura.objects.all()
    # Obtener la cantidad de productos para cada factura
    for factura in facturas:
        # Obtener el producto asociado a la factura
        producto = Productos.objects.get(codigopr=factura.codigopr)
        factura.cantidad_producto = producto.cantidad

    dof = Factura.objects.all()
    x = ''
    for c in dof:        
        x = c.cdcomprador
    context={
        #"factura_agregados":ListaProductos,
        "cliente":ListaCliente,
        "producto":ListaProducto,
        "reporte":ListaProductos,
        "facturas":facturas,
        "di":x
    }  
    return render(request,"reporte.html", context)

@login_required #funcion para que deba de iniciar sesión antes de ongresar a las vistas
@user_passes_test(es_administrador_o_gestor)
def registrarcompra(request):
    try:
        codigoCl = request.POST['Codigo_cliente']
        cliente = Comprador.objects.get(cedula=codigoCl)
        nombre_cliente = cliente.nombre
        apellido_cliente = cliente.apellido
        contratista_cliente = cliente.contratista
        codigoPr = request.POST['Nombre_producto']
        cod = Productos.objects.get(codigopr=codigoPr)
        NomPrd = cod.producto
        cantidad = request.POST['Cant']    
        CantidadBodega = Productos.objects.filter(codigopr=codigoPr)

        for x in CantidadBodega:
            CantidadBodega= x.cantidad

        fecha = date.today()
        prec = Productos.objects.get(codigopr=codigoPr)
        precio = prec.precio
        precioT = int(cantidad) * int(precio)
        descrip = request.POST['desc']  
        EstadoPago = False  

        if int(CantidadBodega) < int(cantidad) :
            messages.error(request,'¡No hay suficientes articulo, solo quedan = {}!'.format(int(CantidadBodega)))  
        else:
            prd = Factura.objects.create(cdcomprador=codigoCl,nombre = nombre_cliente,apellido = apellido_cliente, contratista= contratista_cliente, codigopr=codigoPr,producto=NomPrd, cantidad=cantidad,fecha = fecha,precio=precio,precioTotal=precioT, descripcion=descrip, pago=EstadoPago)
            messages.success(request,'  ¡Registro de compra OK!')
        return redirect('/reporte/')
    except Comprador.DoesNotExist:
        #messages.success(request,'¡Cliente no existente!, as click aqui para registrarlo')
        messages.success(request, '¡Cliente no existente! <a href=/clientes/>Haz clic aquí</a> para registrarlo.')
        return redirect('/reporte/')
    
# Eliminar compra
@login_required #funcion para que deba de iniciar sesión antes de ongresar a las vistas
@user_passes_test(es_administrador_o_gestor)
def eliminacionProductoCompra(request, di):
    #factura = Factura.objects.filter(cdcomprador=codigo, codigopr=cdproducto)
    factura = Factura.objects.get(di=di)
    factura.delete()
    messages.success(request,'¡Registro Eliminado!')
    return redirect('/reporte/')

# Editar producto
@login_required
@user_passes_test(es_administrador_o_gestor)
def edicionProductoCompra(request, di):
    factura = Factura.objects.get(di=di)
    return render(request,"edicionProductoCompra.html",{"factura":factura})

@login_required #funcion para que deba de iniciar sesión antes de ongresar a las vistas
@user_passes_test(es_administrador_o_gestor)
def editarProductoCompra(request):
    codigo = request.POST['txtCodigo']
    codproducto = request.POST['txtProducto']
    cantidad = request.POST['txtCantidad']
    descrip = request.POST['txtDescrip']    
    prd = Factura.objects.get(codigopr=codproducto)
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
@login_required #funcion para que deba de iniciar sesión antes de ongresar a las vistas
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
        venta.pago = False 
        venta.save()
        producto = Productos.objects.get(codigopr=dato.codigopr)
        producto.cantidad = int(producto.cantidad)-int(dato.cantidad)
        producto.save()
    factura = Factura.objects.all().delete()
    messages.success(request,'¡Productos Registrados!')
    return redirect('/reporte/')

@login_required #funcion para que deba de iniciar sesión antes de ongresar a las vistas
def ConsultaVentasCliente(request):  
    factura = Recibo.objects.all().delete()
    codigoCliente = request.POST['Codigo_cliente1']
    fecha_inicio = request.POST['fecha1']
    fecha_fin = request.POST['fecha2']
    DatosFechas = Ventas.objects.filter(cdcomprador=codigoCliente, fecha__range=[fecha_inicio, fecha_fin])
    suma_preciototal = DatosFechas.aggregate(Sum('precioTotal'))['precioTotal__sum']
    for dato in DatosFechas:
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
        vent.pago = dato.pago
        vent.save()
    datos =  Recibo.objects.all()
    suma_preciototal = datos.aggregate(Sum('precioTotal'))['precioTotal__sum']
    factura = Recibo.objects.all()
    return render(request, 'ventas.html', {'ventas': factura,'suma_preciototal': suma_preciototal})

@login_required #funcion para que deba de iniciar sesión antes de ongresar a las vistas    
def ConsultaVentasContratista(request):   
    factura = Recibo.objects.all().delete()
    contratis = request.POST['Nombre_Contratista']
    fecha_inicio = request.POST['fecha1']
    fecha_fin = request.POST['fecha2']
    DatosFechas = Ventas.objects.filter(contratista=contratis, fecha__range=[fecha_inicio, fecha_fin])
    suma_preciototal = DatosFechas.aggregate(Sum('precioTotal'))['precioTotal__sum']
    for dato in DatosFechas:
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
        vent.pago = dato.pago
        vent.save()
    datos =  Recibo.objects.all()
    suma_preciototal = datos.aggregate(Sum('precioTotal'))['precioTotal__sum']
    factura = Recibo.objects.all()
    return render(request, 'ventas.html', {'ventas': factura, 'suma_preciototal': suma_preciototal})

@login_required #funcion para que deba de iniciar sesión antes de ongresar a las vistas
@user_passes_test(es_administrador, no_tiene_permisos)
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
    
    factur = Recibo.objects.all()    

    for d in factur:
        consult = Ventas.objects.filter(cdcomprador=d.cdcomprador, fecha=d.fecha).update(pago=True)    

    datos = Recibo.objects.all().delete()
    return response

@login_required  #funcion para que deba de iniciar sesión antes de ongresar a las vistas 
def LimpiarTablaF(request):
    recibo = Recibo.objects.all()
    recibo.delete()
    messages.success(request,'¡Registro Eliminado!')
    return redirect('/ventas/')

@login_required #funcion para que deba de iniciar sesión antes de ongresar a las vistas
def LimpiarTablaR(request):
    factura = Factura.objects.all()
    factura.delete()
    messages.success(request,'¡Registro Eliminado!')
    return redirect('/reporte/')

@login_required
@user_passes_test(es_administrador_o_gestor)
def clientes(request):
    ListaCliente = Comprador.objects.all()   
    ListaContratista = Contratista.objects.all()  
    context={
        #"factura_agregados":ListaProductos,
        "cliente":ListaCliente,
        "contratista":ListaContratista
    }
    return render(request,"clientes.html", context) 

@login_required
@user_passes_test(es_administrador_o_gestor)
def registrarcliente(request):
    try:
        cedula1 = request.POST['txtCedula']
        nombre1 = request.POST['txtNombre']
        apellido1 = request.POST['txtApellido']
        contratista1 = request.POST['Nombre_Contratista']        
        prd = Comprador.objects.create(cedula=cedula1,nombre=nombre1, apellido=apellido1,contratista=contratista1)
        messages.success(request,'¡Cliente Registrado!')
        return redirect('/clientes/')
    except IntegrityError:
        messages.success(request,'¡Cliente existente!')
        return redirect('/clientes/')
    
@login_required #funcion para que deba de iniciar sesión antes de ingresar a las vistas
@user_passes_test(es_administrador,no_tiene_permisos)
def eliminacioncliente(request, codigo):
    cliente = Comprador.objects.get(cedula=codigo)
    cliente.delete()
    messages.success(request,'¡Cliente Eliminado!')
    return redirect('/clientes/')

@login_required
@user_passes_test(es_administrador,no_tiene_permisos)
def edicionCliente(request, codigo):
    cliente = Comprador.objects.get(cedula=codigo)
    ListaContratista = Contratista.objects.all()  
    context={
        "contratista":ListaContratista,
        "producto":cliente
    }
    return render(request,"edicionCliente.html",context)

@login_required #funcion para que deba de iniciar sesión antes de ongresar a las vistas
@user_passes_test(es_administrador,no_tiene_permisos)
def editarCliente(request):
    cedula = request.POST['txtCedula']
    nombre = request.POST['txtNombre']
    apellido = request.POST['txtApellido']
    contratista = request.POST['Nombre_Contratista']
    prd = Comprador.objects.get(cedula=cedula)
    prd.nombre = nombre
    prd.apellido = apellido
    prd.apellido = apellido
    prd.contratista = contratista
    prd.save()
    messages.success(request,'¡Cliente Actualizado!')
    return redirect('/clientes/')

@login_required #funcion para que deba de iniciar sesión antes de ongresar a las vistas
@user_passes_test(es_administrador,no_tiene_permisos)
def contratista(request):
    ListaContratista = Contratista.objects.all()               
    return render(request,"contratista.html", {"contratista":ListaContratista})

def registrarcontratista(request):
    try:        
        nombreC = request.POST['txtNombre']       
        prd = Contratista.objects.create(nombre=nombreC)
        messages.success(request,'¡Productos Registrado!')
        return redirect('/contratista/')
    except IntegrityError:
        messages.success(request,'¡contratista existente!')
        return redirect('/contratista/')
    
def eliminacioncontratistas(request, codigo):
    contratista = Contratista.objects.get(id=codigo)
    contratista.delete()
    messages.success(request,'¡contratista Eliminado!')
    return redirect('/contratista/')

# Editar contratista
@login_required
@user_passes_test(es_administrador_o_gestor)
def edicionContatista(request, codigo):
    contratista = Contratista.objects.get(id=codigo)
    return render(request,"edicionContatista.html",{"contratista":contratista})

@login_required #funcion para que deba de iniciar sesión antes de ongresar a las vistas
@user_passes_test(es_administrador_o_gestor)
def editarContatista(request):    
    codigo = request.POST['txtCodigo']
    nombreC = request.POST['txtNombre']       
    prd = Contratista.objects.get(id = codigo)
    prd.id = codigo
    prd.nombre = nombreC
    prd.save()
    messages.success(request,'¡Producto Actualizado!')
    return redirect('/contratista/')
    