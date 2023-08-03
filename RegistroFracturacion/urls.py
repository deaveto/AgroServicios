from django.urls import path
from RegistroFracturacion import views

urlpatterns = [
    path('', views.inventario),
    path('ventas/', views.ventas),
    
        
    path('inventario/', views.inventario),
    path('registrarProducto/', views.registrarproducto),
    path('eliminacionProducto/<codigo>', views.eliminacionProducto),
    path('edicionProducto/<codigo>', views.edicionProducto),
    path('editarProducto/', views.editarProducto),  

    path('registrarcompra/', views.registrarcompra),
    path('reporte/', views.reporte),
    path('eliminacionProductoCompra/<codigo>', views.eliminacionProductoCompra),
    path('edicionProductoCompra/<codigo>', views.edicionProductoCompra),
    path('editarProductoCompra/', views.editarProductoCompra),  
    path('copiarDatosFacturaAventes/', views.copiarDatosFacturaAventes),

    path('ConsultaVentasCliente/', views.ConsultaVentasCliente),
    path('ConsultaVentasContratista/', views.ConsultaVentasContratista),

    path('exportar/', views.Exportar, name='exportar'),
    path('LimpiarTablaF/', views.LimpiarTablaF),
    path('LimpiarTablaR/', views.LimpiarTablaR),
]