"""
============================================================
populate_db.py - Script para Poblar la Base de Datos con Datos de Prueba
============================================================
Este script crea datos de ejemplo para probar el proyecto.

CÓMO EJECUTAR:
  python manage.py shell < populate_db.py

O desde la shell interactiva de Django:
  python manage.py shell
  >>> exec(open('populate_db.py').read())

NOTA: Ejecutar solo una vez. Si se ejecuta dos veces puede
generar errores de unicidad (email duplicado, etc.)
============================================================
"""

# Importamos los modelos que vamos a poblar
from gestion.models import Cliente, Cuenta, Transaccion
from decimal import Decimal

print("=" * 50)
print("Iniciando carga de datos de prueba...")
print("=" * 50)

# ============================================================
# PASO 1: Crear Clientes
# ============================================================
print("\n📋 Creando clientes...")

# objects.get_or_create() → crea si no existe, obtiene si ya existe
# Retorna una tupla (objeto, fue_creado)
cliente1, creado = Cliente.objects.get_or_create(
    email="ana.garcia@alkewallet.cl",
    defaults={
        "nombre": "Ana García López",
        "telefono": "+56 9 1234 5678",
        "activo": True
    }
)
print(f"  {'✅ Creado' if creado else '⚠️  Ya existe'}: {cliente1.nombre}")

cliente2, creado = Cliente.objects.get_or_create(
    email="luis.perez@alkewallet.cl",
    defaults={
        "nombre": "Luis Pérez Muñoz",
        "telefono": "+56 9 8765 4321",
        "activo": True
    }
)
print(f"  {'✅ Creado' if creado else '⚠️  Ya existe'}: {cliente2.nombre}")

cliente3, creado = Cliente.objects.get_or_create(
    email="maria.gonzalez@alkewallet.cl",
    defaults={
        "nombre": "María González Silva",
        "telefono": None,   # Teléfono opcional
        "activo": True
    }
)
print(f"  {'✅ Creado' if creado else '⚠️  Ya existe'}: {cliente3.nombre}")

# ============================================================
# PASO 2: Crear Cuentas
# ============================================================
print("\n💳 Creando cuentas...")

cuenta1, creado = Cuenta.objects.get_or_create(
    numero_cuenta="CTA-001",
    defaults={
        "cliente": cliente1,
        "tipo": "ahorro",
        "saldo": Decimal("150000.00"),
        "activa": True
    }
)
print(f"  {'✅ Creada' if creado else '⚠️  Ya existe'}: {cuenta1}")

cuenta2, creado = Cuenta.objects.get_or_create(
    numero_cuenta="CTA-002",
    defaults={
        "cliente": cliente1,
        "tipo": "corriente",
        "saldo": Decimal("300000.00"),
        "activa": True
    }
)
print(f"  {'✅ Creada' if creado else '⚠️  Ya existe'}: {cuenta2}")

cuenta3, creado = Cuenta.objects.get_or_create(
    numero_cuenta="CTA-003",
    defaults={
        "cliente": cliente2,
        "tipo": "ahorro",
        "saldo": Decimal("75000.50"),
        "activa": True
    }
)
print(f"  {'✅ Creada' if creado else '⚠️  Ya existe'}: {cuenta3}")

cuenta4, creado = Cuenta.objects.get_or_create(
    numero_cuenta="CTA-004",
    defaults={
        "cliente": cliente3,
        "tipo": "inversion",
        "saldo": Decimal("500000.00"),
        "activa": True
    }
)
print(f"  {'✅ Creada' if creado else '⚠️  Ya existe'}: {cuenta4}")

# ============================================================
# PASO 3: Crear Transacciones
# ============================================================
print("\n💰 Creando transacciones...")

# bulk_create() inserta varios registros en una sola query SQL
# Más eficiente que crear uno por uno
transacciones = [
    Transaccion(cuenta=cuenta1, tipo="deposito",
                monto=Decimal("50000.00"), descripcion="Depósito inicial"),
    Transaccion(cuenta=cuenta1, tipo="retiro",
                monto=Decimal("10000.00"), descripcion="Retiro cajero"),
    Transaccion(cuenta=cuenta2, tipo="deposito",
                monto=Decimal("200000.00"), descripcion="Sueldo enero"),
    Transaccion(cuenta=cuenta2, tipo="transferencia_envio",
                monto=Decimal("30000.00"), descripcion="Pago arriendo"),
    Transaccion(cuenta=cuenta3, tipo="deposito",
                monto=Decimal("75000.50"), descripcion="Ahorro mensual"),
    Transaccion(cuenta=cuenta4, tipo="deposito",
                monto=Decimal("500000.00"), descripcion="Inversión inicial"),
]

# ignore_conflicts=True evita error si algún registro ya existe
Transaccion.objects.bulk_create(transacciones, ignore_conflicts=False)
print(f"  ✅ {len(transacciones)} transacciones creadas")

# ============================================================
# PASO 4: Verificar con consultas
# ============================================================
print("\n📊 Verificación final:")
print(f"  Clientes totales: {Cliente.objects.count()}")
print(f"  Cuentas totales:  {Cuenta.objects.count()}")
print(f"  Transacciones:    {Transaccion.objects.count()}")

# Consulta con filtro y annotate
from django.db.models import Count, Sum
resumen = Cliente.objects.annotate(
    num_cuentas=Count('cuentas')
).values('nombre', 'num_cuentas')

print("\n  Clientes y sus cuentas:")
for r in resumen:
    print(f"    - {r['nombre']}: {r['num_cuentas']} cuenta(s)")

print("\n✅ Datos de prueba cargados exitosamente.")
print("   Puedes verlos en: http://127.0.0.1:8000/admin/")
print("=" * 50)
