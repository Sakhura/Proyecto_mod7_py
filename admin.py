"""
============================================================
admin.py - Registro de Modelos en el Panel de Administración
============================================================
Django incluye un panel de administración AUTOMÁTICO en /admin.
Para que un modelo aparezca ahí, debemos registrarlo aquí.

El panel admin permite:
  - Ver, crear, editar y eliminar registros sin escribir código
  - Buscar y filtrar datos fácilmente
  - Gestionar usuarios y permisos

Acceso: http://127.0.0.1:8000/admin/
Credenciales: las del superusuario creado con createsuperuser
============================================================
"""

from django.contrib import admin
from .models import Cliente, Cuenta, Transaccion


# ============================================================
# Configuración del Admin para Cliente
# ============================================================
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """
    Personaliza cómo se muestra el modelo Cliente en el admin.
    @admin.register(Cliente) es un decorador equivalente a:
      admin.site.register(Cliente, ClienteAdmin)
    """

    # list_display: columnas que aparecen en la lista de registros
    list_display = ('nombre', 'email', 'telefono', 'activo', 'fecha_registro')

    # list_filter: filtros en el panel derecho del admin
    # Permite filtrar por activo=True/False y por fecha
    list_filter = ('activo', 'fecha_registro')

    # search_fields: activa la barra de búsqueda
    # '^' = empieza con, '=' = exacto, '@' = búsqueda completa, sin prefijo = contiene
    search_fields = ('nombre', 'email', 'telefono')

    # list_editable: permite editar estos campos directamente en la lista
    list_editable = ('activo',)

    # ordering: orden por defecto en la lista
    ordering = ('nombre',)

    # readonly_fields: campos que no se pueden editar desde el admin
    readonly_fields = ('fecha_registro',)


# ============================================================
# Configuración del Admin para Cuenta
# ============================================================
@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    """
    Personaliza la vista del modelo Cuenta en el admin.
    """
    list_display = ('numero_cuenta', 'cliente', 'tipo', 'saldo', 'activa', 'fecha_creacion')
    list_filter = ('tipo', 'activa', 'fecha_creacion')

    # search_fields puede buscar en campos de modelos relacionados
    # con __ (double underscore) accedemos a campos del modelo relacionado
    search_fields = ('numero_cuenta', 'cliente__nombre', 'cliente__email')

    list_editable = ('activa',)
    readonly_fields = ('fecha_creacion',)

    # raw_id_fields: en vez de un dropdown, muestra un campo de búsqueda
    # Útil cuando hay muchos clientes (evita cargar todos en un select)
    raw_id_fields = ('cliente',)


# ============================================================
# Configuración del Admin para Transaccion
# ============================================================
@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    """
    Personaliza la vista del modelo Transaccion en el admin.
    Las transacciones son solo de lectura (no se deben editar).
    """
    list_display = ('fecha', 'cuenta', 'tipo', 'monto', 'descripcion')
    list_filter = ('tipo', 'fecha')
    search_fields = ('cuenta__numero_cuenta', 'cuenta__cliente__nombre', 'descripcion')

    # Las transacciones NO deben editarse una vez creadas
    # (integridad financiera)
    readonly_fields = ('fecha', 'cuenta', 'tipo', 'monto', 'descripcion')

    # date_hierarchy: navegación por fecha en la parte superior
    date_hierarchy = 'fecha'
