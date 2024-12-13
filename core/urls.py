from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('crear_cliente/', views.crear_cliente, name='crear_cliente'),
    path('crear_producto/', views.crear_producto, name='crear_producto'),
    path('clientes/', views.listar_clientes, name='clientes_listar'),
    path('productos/', views.listar_productos, name='productos_listar'),
    path('crear_factura/', views.crear_factura, name='crear_factura'),
    path('crear_abono/', views.crear_abono, name='crear_abono'),
    path('factura/<int:factura_id>/', views.factura_detalle, name='factura_detalle'),
    path('factura/<int:factura_id>/crear_abono/', views.crear_abono, name='crear_abono'),  # Ajustamos esta línea
    path('facturas/', views.factura_list, name='factura_list'),
    path('lista_abonos/', views.lista_abonos, name='lista_abonos'),
    path('detalle_abono/<int:abono_id>/', views.detalle_abono, name='detalle_abono'),
    path('editar_abono/<int:abono_id>/', views.editar_abono, name='editar_abono'),
    path('eliminar_abono/<int:abono_id>/', views.eliminar_abono, name='eliminar_abono'),
    # Agregar URL para listar clientes y productos (puedes implementarlas más tarde)
]
