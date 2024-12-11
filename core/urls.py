from django.urls import path
from . import views

urlpatterns = [
    path('crear_cliente/', views.crear_cliente, name='crear_cliente'),
    path('crear_producto/', views.crear_producto, name='crear_producto'),
     path('clientes/', views.listar_clientes, name='clientes_listar'),
    path('productos/', views.listar_productos, name='productos_listar'),
    # Agregar URL para listar clientes y productos (puedes implementarlas más tarde)
]
