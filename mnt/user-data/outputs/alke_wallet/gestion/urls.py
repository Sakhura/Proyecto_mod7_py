"""
============================================================
urls.py - URLs de la App 'gestion'
============================================================
Este archivo define las rutas específicas de nuestra app.
El archivo principal (alke_wallet/urls.py) delega a este
mediante include('gestion.urls').

Patrón de rutas REST para CRUD:
  GET  /clientes/           → Lista de clientes
  GET  /clientes/<pk>/      → Detalle de un cliente
  GET  /clientes/crear/     → Formulario de creación
  POST /clientes/crear/     → Guardar nuevo cliente
  GET  /clientes/<pk>/editar/ → Formulario de edición
  POST /clientes/<pk>/editar/ → Guardar cambios
  GET  /clientes/<pk>/eliminar/ → Confirmación de eliminación
  POST /clientes/<pk>/eliminar/ → Ejecutar eliminación

name='...' permite referenciar URLs por nombre en código:
  reverse('cliente-list')          → '/gestion/clientes/'
  {% url 'cliente-detail' pk=1 %}  → '/gestion/clientes/1/'
============================================================
"""

from django.urls import path
from . import views

# app_name: namespace para evitar conflictos con otras apps
# Permite usar: {% url 'gestion:cliente-list' %}
app_name = 'gestion'

urlpatterns = [

    # --------------------------------------------------------
    # Dashboard
    # --------------------------------------------------------
    path('', views.DashboardView.as_view(), name='dashboard'),

    # --------------------------------------------------------
    # URLs de Clientes (CRUD completo)
    # --------------------------------------------------------
    # <int:pk> captura un número entero de la URL y lo pasa como 'pk' a la vista
    path('clientes/', views.ClienteListView.as_view(), name='cliente-list'),
    path('clientes/<int:pk>/', views.ClienteDetailView.as_view(), name='cliente-detail'),
    path('clientes/crear/', views.ClienteCreateView.as_view(), name='cliente-create'),
    path('clientes/<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente-update'),
    path('clientes/<int:pk>/eliminar/', views.ClienteDeleteView.as_view(), name='cliente-delete'),

    # --------------------------------------------------------
    # URLs de Cuentas (CRUD)
    # --------------------------------------------------------
    path('cuentas/', views.CuentaListView.as_view(), name='cuenta-list'),
    path('cuentas/crear/', views.CuentaCreateView.as_view(), name='cuenta-create'),
    path('cuentas/<int:pk>/editar/', views.CuentaUpdateView.as_view(), name='cuenta-update'),
    path('cuentas/<int:pk>/eliminar/', views.CuentaDeleteView.as_view(), name='cuenta-delete'),

    # --------------------------------------------------------
    # URLs de Transacciones
    # --------------------------------------------------------
    path('transacciones/', views.TransaccionListView.as_view(), name='transaccion-list'),
    path('transacciones/crear/', views.TransaccionCreateView.as_view(), name='transaccion-create'),
]
