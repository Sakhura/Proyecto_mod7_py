"""
============================================================
urls.py - Configuración Principal de URLs (Enrutador Central)
============================================================
Este archivo es el ROUTER principal del proyecto.
Aquí definimos qué URL lleva a qué parte del sistema.

Funciona como un "índice": cuando llega una petición a una URL,
Django busca aquí para saber a qué app derivarla.

Estructura de URLs del proyecto:
  /admin/             → Panel de administración de Django
  /accounts/login/    → Login de usuarios
  /accounts/logout/   → Logout de usuarios
  /gestion/           → App principal de gestión (CRUD)
============================================================
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # Para redirección de raíz

urlpatterns = [
    # --------------------------------------------------------
    # Panel de Administración de Django
    # --------------------------------------------------------
    # Django genera automáticamente una interfaz visual completa
    # para gestionar todos los modelos registrados en admin.py
    # Acceso: http://127.0.0.1:8000/admin/
    path('admin/', admin.site.urls),

    # --------------------------------------------------------
    # Autenticación (login / logout)
    # --------------------------------------------------------
    # django.contrib.auth provee vistas listas para usar:
    #   /accounts/login/   → Formulario de inicio de sesión
    #   /accounts/logout/  → Cierre de sesión
    # No necesitamos escribir estas vistas nosotros mismos
    path('accounts/', include('django.contrib.auth.urls')),

    # --------------------------------------------------------
    # App de Gestión (nuestra app principal)
    # --------------------------------------------------------
    # include() delega el resto del path a gestion/urls.py
    # Así mantenemos las URLs de cada app organizadas en su propia app
    path('gestion/', include('gestion.urls')),

    # --------------------------------------------------------
    # Raíz del sitio → redirige a lista de clientes
    # --------------------------------------------------------
    # Cuando alguien entra a http://127.0.0.1:8000/ sin ruta,
    # lo mandamos directo a la sección de gestión
    path('', RedirectView.as_view(url='/gestion/clientes/', permanent=False)),
]
