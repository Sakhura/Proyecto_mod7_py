"""
============================================================
views.py - Vistas del Proyecto (Controladores)
============================================================
Las vistas reciben una petición HTTP y retornan una respuesta.
Son el "puente" entre los modelos (datos) y los templates (HTML).

Django ofrece dos tipos de vistas:
  1. FBV (Function-Based Views): funciones Python simples
  2. CBV (Class-Based Views): clases que heredan de views genéricas

Usamos CBV porque:
  - Reutilizan lógica CRUD ya programada por Django
  - Son más ordenadas y fáciles de extender
  - Menos código para operaciones comunes

VISTAS GENÉRICAS CRUD usadas:
  ListView     → Listar todos los registros
  DetailView   → Ver detalle de UN registro
  CreateView   → Formulario para crear nuevo registro
  UpdateView   → Formulario para editar registro existente
  DeleteView   → Confirmación de eliminación

SEGURIDAD: LoginRequiredMixin protege vistas para que solo
usuarios autenticados puedan acceder.
============================================================
"""

from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import connection          # Para consultas SQL directas con cursor
from django.db.models import Sum, Count   # Para anotaciones y agregaciones
from django.contrib import messages       # Para mensajes flash
from .models import Cliente, Cuenta, Transaccion
from .forms import ClienteForm, CuentaForm, TransaccionForm


# ============================================================
# DASHBOARD - Vista Principal con consultas personalizadas
# ============================================================
class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Vista del panel principal con estadísticas del sistema.
    Demuestra consultas avanzadas con anotaciones y agregaciones.
    """
    template_name = 'gestion/dashboard.html'

    def get_context_data(self, **kwargs):
        """
        get_context_data: agrega variables al contexto del template.
        kwargs contiene las variables ya existentes del contexto.
        """
        context = super().get_context_data(**kwargs)

        # ---- Consultas ORM con agregaciones ----
        # Count('id') cuenta los registros que cumplen la condición
        context['total_clientes'] = Cliente.objects.filter(activo=True).count()
        context['total_cuentas'] = Cuenta.objects.filter(activa=True).count()

        # aggregate() retorna un diccionario con los resultados
        # Sum('monto') suma todos los montos de las transacciones
        total = Transaccion.objects.aggregate(total=Sum('monto'))
        context['total_transacciones'] = total['total'] or 0

        # ---- Consultas con annotate() ----
        # annotate() agrega un campo calculado a cada objeto del queryset
        # Aquí agregamos 'num_cuentas' = cantidad de cuentas por cliente
        context['clientes_con_cuentas'] = Cliente.objects.annotate(
            num_cuentas=Count('cuentas')
        ).order_by('-num_cuentas')[:5]  # Top 5 clientes con más cuentas

        # ---- Consulta con cursor (SQL puro) ----
        # Útil cuando el ORM no cubre consultas muy específicas
        # Siempre usar parámetros con %s para evitar SQL Injection
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT tipo, COUNT(*) as cantidad, SUM(monto) as total
                FROM gestion_transaccion
                GROUP BY tipo
                ORDER BY total DESC
            """)
            # fetchall() retorna lista de tuplas con los resultados
            context['estadisticas_transacciones'] = cursor.fetchall()

        # ---- Últimas transacciones ----
        # select_related() hace JOIN en una sola query (evita N+1 queries)
        context['ultimas_transacciones'] = Transaccion.objects.select_related(
            'cuenta__cliente'
        ).order_by('-fecha')[:10]

        return context


# ============================================================
# VISTAS CRUD - Cliente
# ============================================================
class ClienteListView(LoginRequiredMixin, ListView):
    """
    Lista todos los clientes. URL: /gestion/clientes/
    ListView necesita:
      - model: ¿qué modelo listar?
      - template_name: template a renderizar
      - context_object_name: nombre de la variable en el template
    """
    model = Cliente
    template_name = 'gestion/cliente_list.html'
    context_object_name = 'clientes'  # En el template: {{ clientes }}

    # paginate_by: paginación automática (Django la maneja)
    paginate_by = 10

    def get_queryset(self):
        """
        Sobreescribimos get_queryset para agregar búsqueda por texto.
        El queryset es la "consulta" que define qué objetos mostrar.
        """
        # queryset base: todos los clientes ordenados por nombre
        queryset = Cliente.objects.all()

        # Búsqueda: si hay parámetro 'q' en la URL (?q=Ana)
        # request.GET es un diccionario con los parámetros de la URL
        busqueda = self.request.GET.get('q', '')
        if busqueda:
            # filter() con __icontains = búsqueda insensible a mayúsculas
            # que "contiene" el texto buscado
            queryset = queryset.filter(
                nombre__icontains=busqueda
            ) | queryset.filter(
                email__icontains=busqueda
            )
        return queryset

    def get_context_data(self, **kwargs):
        """Agrega el término de búsqueda al contexto para mostrarlo en el template."""
        context = super().get_context_data(**kwargs)
        context['busqueda'] = self.request.GET.get('q', '')
        return context


class ClienteDetailView(LoginRequiredMixin, DetailView):
    """
    Muestra el detalle de UN cliente. URL: /gestion/clientes/<pk>/
    DetailView busca automáticamente el objeto por su primary key (pk)
    que viene en la URL.
    """
    model = Cliente
    template_name = 'gestion/cliente_detail.html'
    context_object_name = 'cliente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregamos las cuentas del cliente al contexto
        # self.object es el cliente encontrado por DetailView
        context['cuentas'] = self.object.cuentas.all()
        return context


class ClienteCreateView(LoginRequiredMixin, CreateView):
    """
    Formulario para crear nuevo cliente. URL: /gestion/clientes/crear/
    CreateView maneja automáticamente:
      - GET: muestra el formulario vacío
      - POST: valida y guarda el nuevo registro
    """
    model = Cliente
    form_class = ClienteForm
    template_name = 'gestion/cliente_form.html'

    # reverse_lazy: URL a la que redirigir después de guardar
    # 'lazy' porque la URL no se resuelve hasta que se necesita
    success_url = reverse_lazy('cliente-list')

    def form_valid(self, form):
        """
        Se ejecuta cuando el formulario es válido.
        Aquí podemos agregar lógica adicional antes de guardar.
        """
        # messages.success: muestra notificación en el siguiente request
        messages.success(self.request, f'Cliente "{form.instance.nombre}" creado exitosamente.')
        return super().form_valid(form)


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    """
    Formulario para editar un cliente existente. URL: /gestion/clientes/<pk>/editar/
    UpdateView carga automáticamente el objeto por pk y rellena el formulario.
    """
    model = Cliente
    form_class = ClienteForm
    template_name = 'gestion/cliente_form.html'
    success_url = reverse_lazy('cliente-list')

    def form_valid(self, form):
        messages.success(self.request, f'Cliente "{form.instance.nombre}" actualizado.')
        return super().form_valid(form)


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    """
    Confirmación de eliminación. URL: /gestion/clientes/<pk>/eliminar/
    DeleteView:
      - GET: muestra página de confirmación
      - POST: elimina el registro y redirige
    """
    model = Cliente
    template_name = 'gestion/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente-list')

    def form_valid(self, form):
        nombre = self.object.nombre
        messages.warning(self.request, f'Cliente "{nombre}" eliminado.')
        return super().form_valid(form)


# ============================================================
# VISTAS CRUD - Cuenta
# ============================================================
class CuentaListView(LoginRequiredMixin, ListView):
    model = Cuenta
    template_name = 'gestion/cuenta_list.html'
    context_object_name = 'cuentas'
    paginate_by = 10

    def get_queryset(self):
        # select_related() evita múltiples queries al BD
        # Hace un JOIN con Cliente en una sola consulta
        return Cuenta.objects.select_related('cliente').all()


class CuentaCreateView(LoginRequiredMixin, CreateView):
    model = Cuenta
    form_class = CuentaForm
    template_name = 'gestion/cuenta_form.html'
    success_url = reverse_lazy('cuenta-list')

    def form_valid(self, form):
        messages.success(self.request, 'Cuenta creada exitosamente.')
        return super().form_valid(form)


class CuentaUpdateView(LoginRequiredMixin, UpdateView):
    model = Cuenta
    form_class = CuentaForm
    template_name = 'gestion/cuenta_form.html'
    success_url = reverse_lazy('cuenta-list')

    def form_valid(self, form):
        messages.success(self.request, 'Cuenta actualizada exitosamente.')
        return super().form_valid(form)


class CuentaDeleteView(LoginRequiredMixin, DeleteView):
    model = Cuenta
    template_name = 'gestion/cuenta_confirm_delete.html'
    success_url = reverse_lazy('cuenta-list')


# ============================================================
# VISTAS CRUD - Transacción
# ============================================================
class TransaccionListView(LoginRequiredMixin, ListView):
    model = Transaccion
    template_name = 'gestion/transaccion_list.html'
    context_object_name = 'transacciones'
    paginate_by = 15

    def get_queryset(self):
        # select_related con doble nivel: transaccion → cuenta → cliente
        # Todo en una sola query SQL (muy eficiente)
        return Transaccion.objects.select_related(
            'cuenta', 'cuenta__cliente'
        ).order_by('-fecha')


class TransaccionCreateView(LoginRequiredMixin, CreateView):
    model = Transaccion
    form_class = TransaccionForm
    template_name = 'gestion/transaccion_form.html'
    success_url = reverse_lazy('transaccion-list')

    def form_valid(self, form):
        messages.success(self.request, 'Transacción registrada exitosamente.')
        return super().form_valid(form)
