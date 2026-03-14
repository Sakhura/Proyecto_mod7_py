# 🏦 Alke Wallet

**Proyecto final del Módulo 7 — Desarrollo Web con Django**  
Alkemy | Billetera Digital para gestión de activos financieros

---

## 📋 Descripción del Proyecto

**Alke Wallet** es una aplicación web desarrollada con **Django** que permite a la empresa fintech *Alke Financial* gestionar clientes, cuentas digitales y transacciones de manera segura y escalable.

### ¿Qué hace la aplicación?

- Gestiona **clientes** con sus datos personales
- Administra **cuentas digitales** (ahorro, corriente, inversión)
- Registra **transacciones** (depósitos, retiros, transferencias)
- Muestra un **dashboard** con estadísticas en tiempo real
- Protege el acceso con **autenticación de usuarios**
- Incluye un **panel de administración** completo

---

## 🏗️ Arquitectura del Proyecto

```
alke_wallet/                    ← Carpeta raíz del proyecto
│
├── alke_wallet/                ← Paquete de configuración Django
│   ├── __init__.py             ← Marca la carpeta como paquete Python
│   ├── settings.py             ← ⚙️ Configuración central (BD, apps, etc.)
│   ├── urls.py                 ← 🗺️ Enrutador principal de URLs
│   └── wsgi.py                 ← Interfaz para despliegue en producción
│
├── gestion/                    ← 📦 App principal del proyecto
│   ├── migrations/             ← Historial de cambios de la BD (auto-generado)
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py                ← 🔧 Registro de modelos en el panel admin
│   ├── apps.py                 ← Configuración de la app
│   ├── forms.py                ← 📝 Formularios Django (validación)
│   ├── models.py               ← 🗄️ Modelos ORM (tablas de BD)
│   ├── urls.py                 ← URLs específicas de la app
│   └── views.py                ← 👁️ Vistas (controladores CRUD)
│
├── templates/                  ← Templates HTML
│   ├── base.html               ← Layout base (navbar, footer)
│   ├── registration/
│   │   └── login.html          ← Página de inicio de sesión
│   └── gestion/
│       ├── dashboard.html      ← Panel principal con estadísticas
│       ├── cliente_list.html   ← Lista con búsqueda y paginación
│       ├── cliente_detail.html ← Detalle de un cliente
│       ├── cliente_form.html   ← Formulario crear/editar
│       ├── cliente_confirm_delete.html
│       ├── cuenta_list.html
│       ├── cuenta_form.html
│       ├── cuenta_confirm_delete.html
│       ├── transaccion_list.html
│       └── transaccion_form.html
│
├── static/
│   └── css/
│       └── style.css           ← Estilos personalizados
│
├── manage.py                   ← CLI de Django (comandos del proyecto)
├── requirements.txt            ← Dependencias del proyecto
├── populate_db.py              ← Script para cargar datos de prueba
├── .env.example                ← Plantilla de variables de entorno
└── .gitignore                  ← Archivos excluidos de Git
```

---

## 🗄️ Modelo de Datos

```
Cliente                  Cuenta                    Transaccion
─────────────            ──────────────────        ───────────────────
id (PK)                  id (PK)                   id (PK)
nombre                   cliente_id (FK→Cliente)   cuenta_id (FK→Cuenta)
email (unique)           numero_cuenta (unique)    tipo
telefono (opcional)      tipo                      monto
fecha_registro           saldo                     descripcion
activo                   activa                    fecha
                         fecha_creacion
```

**Relaciones:**
- `Cliente` → `Cuenta`: **ManyToOne** (ForeignKey) — un cliente tiene muchas cuentas
- `Cuenta` → `Transaccion`: **ManyToOne** (ForeignKey) — una cuenta tiene muchas transacciones

---

## 🚀 Instalación y Ejecución — Paso a Paso

### Requisitos Previos

- Python 3.10 o superior instalado
- Git instalado
- Visual Studio Code (recomendado)

---

### PASO 1 — Clonar o Descargar el Proyecto

```bash
# Opción A: clonar desde GitHub
git clone https://github.com/tu-usuario/alke-wallet.git
cd alke-wallet

# Opción B: si descargaste el ZIP, descomprímelo y entra a la carpeta
cd alke_wallet
```

---

### PASO 2 — Crear el Entorno Virtual

> El entorno virtual aísla las dependencias del proyecto de tu Python global.
> Cada proyecto tiene sus propias versiones de librerías.

```bash
# Crear el entorno virtual (se crea carpeta 'venv/')
python -m venv venv
```

**Activar el entorno virtual:**

```bash
# En Windows (CMD o PowerShell)
venv\Scripts\activate

# En macOS / Linux
source venv/bin/activate
```

> ✅ Sabrás que está activo porque aparece `(venv)` al inicio de tu terminal.

---

### PASO 3 — Instalar Dependencias

```bash
# Instala Django, psycopg2-binary y python-dotenv
pip install -r requirements.txt
```

Verifica que Django se instaló correctamente:
```bash
python -m django --version
# Debe mostrar: 4.2.x
```

---

### PASO 4 — Configurar Variables de Entorno

```bash
# Copia la plantilla de variables de entorno
cp .env.example .env
```

Abre `.env` en VS Code y revisa los valores (para desarrollo, los valores por defecto son suficientes):

```env
SECRET_KEY=django-insecure-cambia-esta-clave-por-una-segura-unica
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

> ⚠️ En producción DEBES cambiar `SECRET_KEY` por un valor único y seguro.

---

### PASO 5 — Aplicar Migraciones (Crear la Base de Datos)

> Las migraciones son la forma de Django de crear y actualizar tablas en la BD.
> Se generan automáticamente desde los modelos definidos en `models.py`.

```bash
# Genera los archivos de migración basándose en los modelos
python manage.py makemigrations

# Aplica las migraciones (crea las tablas en db.sqlite3)
python manage.py migrate
```

Deberías ver una lista de migraciones aplicadas, incluyendo las de Django (auth, admin, sessions) y la nuestra (`gestion`).

---

### PASO 6 — Crear Superusuario (Admin)

```bash
python manage.py createsuperuser
```

Ingresa los datos solicitados:
```
Nombre de usuario: admin
Correo electrónico: admin@alkewallet.cl
Password: ********  (mínimo 8 caracteres)
```

---

### PASO 7 — Cargar Datos de Prueba (Opcional)

```bash
python manage.py shell < populate_db.py
```

Este script crea 3 clientes, 4 cuentas y 6 transacciones de ejemplo para que puedas probar la aplicación inmediatamente.

---

### PASO 8 — Ejecutar el Servidor de Desarrollo

```bash
python manage.py runserver
```

Verás en la terminal:
```
Django version 4.2.x, using settings 'alke_wallet.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

---

## 🌐 URLs de la Aplicación

| URL | Descripción |
|-----|-------------|
| `http://127.0.0.1:8000/` | Redirige al Dashboard |
| `http://127.0.0.1:8000/accounts/login/` | Inicio de sesión |
| `http://127.0.0.1:8000/gestion/` | Dashboard con estadísticas |
| `http://127.0.0.1:8000/gestion/clientes/` | Lista de clientes |
| `http://127.0.0.1:8000/gestion/clientes/crear/` | Crear nuevo cliente |
| `http://127.0.0.1:8000/gestion/cuentas/` | Lista de cuentas |
| `http://127.0.0.1:8000/gestion/transacciones/` | Lista de transacciones |
| `http://127.0.0.1:8000/admin/` | Panel de administración Django |

---

## 🔧 Comandos Django Útiles

```bash
# Ver todas las migraciones y su estado
python manage.py showmigrations

# Abrir consola interactiva de Django (para probar queries ORM)
python manage.py shell

# Recolectar archivos estáticos (para producción)
python manage.py collectstatic

# Ver las queries SQL que genera el ORM
python manage.py shell
>>> from gestion.models import Cliente
>>> qs = Cliente.objects.all()
>>> print(qs.query)
```

---

## 🧪 Pruebas en la Shell de Django

Ejecuta `python manage.py shell` y prueba estas consultas:

```python
from gestion.models import Cliente, Cuenta, Transaccion
from django.db.models import Count, Sum
from django.db import connection

# --- CRUD básico ---

# Crear
c = Cliente.objects.create(nombre="Prueba", email="prueba@test.cl")

# Leer todos
Cliente.objects.all()

# Filtrar (insensible a mayúsculas)
Cliente.objects.filter(nombre__icontains="ana")

# Actualizar
c.telefono = "+56 9 0000 0000"
c.save()

# Eliminar
c.delete()

# --- Consultas avanzadas ---

# Clientes con cantidad de cuentas (annotate)
Cliente.objects.annotate(num_cuentas=Count('cuentas')).values('nombre', 'num_cuentas')

# Suma total de saldos
Cuenta.objects.aggregate(total=Sum('saldo'))

# Excluir inactivos
Cliente.objects.exclude(activo=False)

# SQL personalizado con raw()
Cliente.objects.raw("SELECT * FROM gestion_cliente WHERE activo = 1")

# SQL personalizado con cursor
with connection.cursor() as cursor:
    cursor.execute("SELECT COUNT(*) FROM gestion_cliente")
    print("Total:", cursor.fetchone()[0])
```

---

## 🔐 Configuración de Seguridad

| Característica | Implementación |
|---|---|
| Protección CSRF | `{% csrf_token %}` en todos los formularios POST |
| Autenticación | `LoginRequiredMixin` en todas las vistas |
| Contraseñas | Validadores configurados en `AUTH_PASSWORD_VALIDATORS` |
| Variables sensibles | Manejadas con `.env` y `python-dotenv` |
| SQL Injection | Prevenido por el ORM de Django (parámetros seguros) |

---

## ⚙️ Configuración para Producción (PostgreSQL)

1. Instalar PostgreSQL y crear la base de datos:
```sql
CREATE DATABASE alke_wallet_db;
CREATE USER alke_user WITH PASSWORD 'tu_password_seguro';
GRANT ALL PRIVILEGES ON DATABASE alke_wallet_db TO alke_user;
```

2. Actualizar `.env`:
```env
DEBUG=False
SECRET_KEY=clave-secreta-muy-larga-y-unica
DB_NAME=alke_wallet_db
DB_USER=alke_user
DB_PASSWORD=tu_password_seguro
DB_HOST=localhost
DB_PORT=5432
```

3. Re-ejecutar las migraciones:
```bash
python manage.py migrate
python manage.py collectstatic
```

---

## 📚 Conceptos Django Demostrados

| Concepto | Dónde se implementa |
|---|---|
| ORM y modelos | `gestion/models.py` |
| ForeignKey (ManyToOne) | `Cuenta.cliente`, `Transaccion.cuenta` |
| Migraciones | `gestion/migrations/` |
| Class-Based Views | `gestion/views.py` (ListView, CreateView, etc.) |
| ModelForms | `gestion/forms.py` |
| Protección CSRF | `{% csrf_token %}` en todos los templates |
| django.contrib.admin | `gestion/admin.py` |
| django.contrib.auth | `LoginRequiredMixin`, `/accounts/login/` |
| django.contrib.staticfiles | `static/css/style.css` |
| Consultas avanzadas | `views.py` (annotate, aggregate, raw, cursor) |
| Herencia de templates | `{% extends 'base.html' %}` |
| Control de versiones | `.gitignore`, estructura de ramas |

---

## 👩‍💻 Tecnologías Utilizadas

- **Python 3.10+**
- **Django 4.2 LTS**
- **SQLite** (desarrollo) / **PostgreSQL** (producción)
- **Bootstrap 5** (diseño responsive)
- **Bootstrap Icons**
- **python-dotenv** (variables de entorno)

---

## 📁 Control de Versiones — Estructura de Ramas Git

```bash
# Rama principal con código estable
git checkout main

# Rama para el desarrollo de modelos
git checkout -b feature/modelos

# Rama para las vistas CRUD
git checkout -b feature/crud

# Subir al repositorio
git add .
git commit -m "feat: agrega modelo Cliente con validaciones"
git push origin feature/modelos
```

---

*Proyecto desarrollado para Alkemy — Módulo 7: Desarrollo Web con Django* 🐍
