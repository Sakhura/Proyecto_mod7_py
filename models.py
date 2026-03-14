"""
============================================================
models.py - Modelos de Datos (ORM de Django)
============================================================
Los modelos son clases Python que representan tablas en la BD.
Django convierte automáticamente estas clases en SQL mediante
el ORM (Object-Relational Mapper).

VENTAJA DEL ORM: Escribimos Python en vez de SQL.
  Python:  Cliente.objects.filter(nombre__startswith='A')
  SQL:     SELECT * FROM gestion_cliente WHERE nombre LIKE 'A%'

MODELOS DEL PROYECTO:
  Cliente     → Personas que usan la billetera
  Cuenta      → Cuentas digitales de cada cliente (relación ManyToOne)
  Transaccion → Movimientos de dinero entre cuentas (relación ManyToOne)

RELACIONES:
  - Cliente → Cuenta:      Un cliente puede tener MUCHAS cuentas (ForeignKey)
  - Cuenta  → Transaccion: Una cuenta puede tener MUCHAS transacciones (ForeignKey)

Después de modificar este archivo, SIEMPRE ejecutar:
  python manage.py makemigrations
  python manage.py migrate
============================================================
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


# ============================================================
# MODELO: Cliente
# ============================================================
class Cliente(models.Model):
    """
    Representa a un usuario de la billetera digital Alke Wallet.

    Tabla en BD: gestion_cliente
    Django nombra las tablas como: {nombre_app}_{nombre_modelo_en_minúsculas}
    """

    # CharField = texto de longitud máxima fija
    # max_length=100 → máximo 100 caracteres
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre completo',  # Etiqueta en el admin y formularios
        help_text='Ingrese el nombre completo del cliente'
    )

    # EmailField valida automáticamente que el formato sea email válido
    # unique=True → no pueden existir dos clientes con el mismo email
    email = models.EmailField(
        unique=True,
        verbose_name='Correo electrónico'
    )

    # blank=True → el campo puede estar vacío en formularios
    # null=True  → la columna puede ser NULL en la base de datos
    # Ambos juntos = campo opcional
    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Teléfono'
    )

    # DateField → almacena solo fecha (sin hora)
    # auto_now_add=True → se establece automáticamente al crear el registro
    # No se puede editar después de crear
    fecha_registro = models.DateField(
        auto_now_add=True,
        verbose_name='Fecha de registro'
    )

    # BooleanField → True/False
    # default=True → por defecto los clientes están activos
    activo = models.BooleanField(
        default=True,
        verbose_name='¿Está activo?'
    )

    class Meta:
        """
        Meta = configuración del modelo que no es un campo.
        """
        # Nombre legible en singular para el admin de Django
        verbose_name = 'Cliente'
        # Nombre legible en plural para el admin de Django
        verbose_name_plural = 'Clientes'
        # Ordenamiento por defecto al listar: por nombre ascendente
        ordering = ['nombre']

    def __str__(self):
        """
        __str__ define cómo se muestra el objeto como texto.
        Se usa en el admin, en el shell y en los templates.
        Ejemplo: "Ana García"
        """
        return self.nombre

    def get_saldo_total(self):
        """
        Método personalizado que calcula el saldo total del cliente
        sumando los saldos de todas sus cuentas activas.

        Esto demuestra cómo podemos agregar lógica de negocio
        directamente en el modelo (fat models, thin views).
        """
        # self.cuentas → acceso a las cuentas relacionadas
        # (el related_name='cuentas' definido en el modelo Cuenta)
        return sum(
            cuenta.saldo
            for cuenta in self.cuentas.filter(activa=True)
        )


# ============================================================
# MODELO: Cuenta
# ============================================================
class Cuenta(models.Model):
    """
    Representa una cuenta digital dentro de Alke Wallet.
    Un cliente puede tener múltiples cuentas.

    RELACIÓN con Cliente: ManyToOne (ForeignKey)
    → Muchas cuentas pertenecen a UN cliente
    → Un cliente puede tener MUCHAS cuentas

    Tabla en BD: gestion_cuenta
    """

    # Opciones para el tipo de cuenta
    # Se define como tuplas (valor_bd, etiqueta_legible)
    TIPO_CUENTA_CHOICES = [
        ('ahorro', 'Cuenta de Ahorro'),
        ('corriente', 'Cuenta Corriente'),
        ('inversion', 'Cuenta de Inversión'),
    ]

    # ForeignKey = relación Muchos a Uno
    # on_delete=CASCADE → si se elimina el cliente, se eliminan sus cuentas
    # related_name='cuentas' → permite acceder desde cliente.cuentas.all()
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='cuentas',  # nombre para acceso inverso
        verbose_name='Cliente titular'
    )

    # Número único de cuenta (como un RUT o número de tarjeta)
    numero_cuenta = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de cuenta'
    )

    # choices restringe los valores a las opciones definidas
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CUENTA_CHOICES,
        default='ahorro',
        verbose_name='Tipo de cuenta'
    )

    # DecimalField → valores monetarios (más preciso que FloatField)
    # max_digits=12 → hasta 12 dígitos en total
    # decimal_places=2 → 2 decimales (centavos)
    # validators → valida que el saldo no sea negativo
    saldo = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Saldo disponible'
    )

    activa = models.BooleanField(
        default=True,
        verbose_name='¿Está activa?'
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )

    class Meta:
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'
        ordering = ['-fecha_creacion']  # Las más recientes primero

    def __str__(self):
        """Ejemplo: "Cuenta de Ahorro - Ana García (#CTA-001)"""
        return f"{self.get_tipo_display()} - {self.cliente.nombre} (#{self.numero_cuenta})"

    def depositar(self, monto):
        """
        Método de negocio: agrega saldo a la cuenta.
        Encapsulamos la lógica aquí para reutilizarla desde cualquier vista.
        """
        if monto <= 0:
            raise ValueError("El monto del depósito debe ser positivo")
        self.saldo += Decimal(str(monto))
        self.save()

    def retirar(self, monto):
        """
        Método de negocio: retira saldo de la cuenta.
        Valida que haya saldo suficiente antes de proceder.
        """
        if monto <= 0:
            raise ValueError("El monto del retiro debe ser positivo")
        if self.saldo < Decimal(str(monto)):
            raise ValueError("Saldo insuficiente para realizar el retiro")
        self.saldo -= Decimal(str(monto))
        self.save()


# ============================================================
# MODELO: Transaccion
# ============================================================
class Transaccion(models.Model):
    """
    Registra cada movimiento de dinero en el sistema.
    Cada transacción pertenece a UNA cuenta (ManyToOne con ForeignKey).

    RELACIÓN con Cuenta: ManyToOne (ForeignKey)
    → Muchas transacciones pertenecen a UNA cuenta
    → Una cuenta puede tener MUCHAS transacciones

    Tabla en BD: gestion_transaccion
    """

    TIPO_TRANSACCION_CHOICES = [
        ('deposito', 'Depósito'),
        ('retiro', 'Retiro'),
        ('transferencia_envio', 'Transferencia Enviada'),
        ('transferencia_recepcion', 'Transferencia Recibida'),
    ]

    # Cuenta de origen de la transacción
    cuenta = models.ForeignKey(
        Cuenta,
        on_delete=models.PROTECT,  # PROTECT evita borrar cuentas con transacciones
        related_name='transacciones',
        verbose_name='Cuenta'
    )

    tipo = models.CharField(
        max_length=30,
        choices=TIPO_TRANSACCION_CHOICES,
        verbose_name='Tipo de transacción'
    )

    monto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Monto'
    )

    # TextField → texto sin límite de longitud (para comentarios largos)
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción'
    )

    # auto_now_add=True → fecha/hora se guarda automáticamente al crear
    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha y hora'
    )

    class Meta:
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'
        ordering = ['-fecha']  # Las más recientes primero

    def __str__(self):
        """Ejemplo: "Depósito de $50000.00 en Cuenta de Ahorro - Ana García"""
        return f"{self.get_tipo_display()} de ${self.monto} en {self.cuenta}"
