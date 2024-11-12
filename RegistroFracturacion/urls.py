from django.urls import path
from RegistroFracturacion import views

urlpatterns = [
    path('', views.inventario),
    path('ventas/', views.ventas),
    path('base1/', views.home1),
    
        
    path('inventario/', views.inventario),
    path('registrarProducto/', views.registrarproducto),
    path('eliminacionProducto/<codigo>', views.eliminacionProducto),
    path('edicionProducto/<codigo>', views.edicionProducto),
    path('editarProducto/', views.editarProducto),  

    path('registrarcompra/', views.registrarcompra),
    path('reporte/', views.reporte),
    path('eliminacionProductoCompra/<di>', views.eliminacionProductoCompra),
    path('edicionProductoCompra/<di>', views.edicionProductoCompra),
    path('editarProductoCompra/', views.editarProductoCompra),  
    path('copiarDatosFacturaAventes/', views.copiarDatosFacturaAventes),

    path('ConsultaVentasCliente/', views.ConsultaVentasCliente),
    path('ConsultaVentasContratista/', views.ConsultaVentasContratista),

    path('exportar/', views.Exportar, name='exportar'),
    path('LimpiarTablaF/', views.LimpiarTablaF),
    path('LimpiarTablaR/', views.LimpiarTablaR),

    path('no_tiene_permisos/', views.no_tiene_permisos),

    path('clientes/', views.clientes),
    path('registrarcliente/', views.registrarcliente),
    path('eliminacioncliente/<codigo>', views.eliminacioncliente),
    path('edicionCliente/<codigo>', views.edicionCliente),
    path('editarCliente/', views.editarCliente), 

    path('contratista/', views.contratista),
    path('registrarcontratista/', views.registrarcontratista),
    path('eliminacioncontratistas/<codigo>', views.eliminacioncontratistas),
    path('edicionContatista/<codigo>', views.edicionContatista),
    path('editarContatista/', views.editarContatista),
]