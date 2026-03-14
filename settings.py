"""
============================================================
settings.py - Configuración Central del Proyecto Django
============================================================
Este archivo controla TODOS los aspectos del proyecto:
  - Conexión a la base de datos
  - Apps instaladas
  - Templates HTML
  - Archivos estáticos (CSS, JS, imágenes)
  - Seguridad
  - Autenticación

Buena práctica: separar configuraciones sensibles en .env
para no exponer contraseñas en el código fuente.
============================================================
"""

import os
from pathlib import Path

# python-dotenv carga las variables del archivo .env
# Así mantenemos las contraseñas fuera del código
from dotenv import load_dotenv
load_dotenv()

# ============================================================
# RUTAS DEL PROYECTO
# ============================================================
# BASE_DIR apunta a la raíz del proyecto (donde está manage.py)
# Path(__file__) = ruta de este archivo (settings.py)
# .resolve().parent.parent = subimos 2 niveles hasta la raíz
BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SEGURIDAD
# ============================================================
# SECRET_KEY: clave criptográfica para sesiones, tokens CSRF, etc.
# Se lee desde .env para no exponerla en el código
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-clave-solo-para-desarrollo')

# DEBUG=True muestra errores detallados → SOLO en desarrollo
# En producción DEBE ser False para no exponer información sensible
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Lista de dominios/IPs que pueden acceder al proyecto
# En desarrollo: localhost y 127.0.0.1 son suficientes
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# ============================================================
# APLICACIONES INSTALADAS
# ============================================================
# Django funciona con "apps" modulares. Cada app cumple una función.
INSTALLED_APPS = [
    # --- Apps preinstaladas de Django ---

    # Panel de administración visual en /admin
    # Permite gestionar todos los modelos sin código SQL
    'django.contrib.admin',

    # Sistema de autenticación: usuarios, contraseñas, permisos
    # Provee login, logout, grupos y permisos
    'django.contrib.auth',

    # Framework de tipos de contenido (requerido por admin y auth)
    'django.contrib.contenttypes',

    # Manejo de sesiones de usuario (cookies de sesión)
    'django.contrib.sessions',

    # Mensajes flash (notificaciones como "Guardado exitosamente")
    'django.contrib.messages',

    # Sirve archivos estáticos: CSS, JavaScript, imágenes
    'django.contrib.staticfiles',

    # --- Nuestra aplicación del proyecto ---
    # Contiene los modelos Cliente, Cuenta, Transaccion
    'gestion',
]


# ============================================================
# MIDDLEWARE
# ============================================================
# Son capas que procesan cada request/response de forma secuencial
# Piensa en ellos como "filtros" que se ejecutan en cada petición
MIDDLEWARE = [
    # Maneja seguridad HTTPS y cabeceras de seguridad
    'django.middleware.security.SecurityMiddleware',

    # Gestiona las sesiones de usuario (cookies)
    'django.contrib.sessions.middleware.SessionMiddleware',

    # Funcionalidades comunes: trailing slash, ETags, etc.
    'django.middleware.common.CommonMiddleware',

    # Protección CSRF: valida token en formularios POST
    # FUNDAMENTAL para evitar ataques Cross-Site Request Forgery
    'django.middleware.csrf.CsrfViewMiddleware',

    # Asocia usuarios autenticados con cada request
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # Permite pasar mensajes entre views (notificaciones)
    'django.contrib.messages.middleware.MessageMiddleware',

    # Protección contra clickjacking (ataques de iframes maliciosos)
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ============================================================
# URLS PRINCIPALES
# ============================================================
# Le dice a Django dónde encontrar el archivo principal de URLs
ROOT_URLCONF = 'alke_wallet.urls'


# ============================================================
# CONFIGURACIÓN DE TEMPLATES
# ============================================================
# Templates = archivos HTML que Django renderiza con datos dinámicos
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Django buscará templates en la carpeta 'templates/' de la raíz
        'DIRS': [BASE_DIR / 'templates'],

        # También buscará en carpeta 'templates/' dentro de cada app
        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                # Agrega info del request (URL actual, método, etc.)
                'django.template.context_processors.debug',
                'django.template.context_processors.request',

                # Agrega el usuario autenticado a todos los templates
                'django.contrib.auth.context_processors.auth',

                # Permite usar mensajes flash en templates
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ============================================================
# BASE DE DATOS
# ============================================================
# Django soporta múltiples bases de datos.
# Configuramos SQLite para desarrollo (no requiere instalación)
# y PostgreSQL para producción (más robusto y escalable)

if DEBUG:
    # --- DESARROLLO: SQLite ---
    # SQLite es un archivo local, perfecto para desarrollar
    # No necesita servidor, se crea automáticamente con migrate
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            # db.sqlite3 se crea en la raíz del proyecto
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # --- PRODUCCIÓN: PostgreSQL ---
    # PostgreSQL es más robusto, maneja concurrencia y grandes volúmenes
    # Requiere instalar psycopg2: pip install psycopg2-binary
    # Los valores vienen del archivo .env (NUNCA hardcodeados)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'alke_wallet_db'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }


# ============================================================
# VALIDADORES DE CONTRASEÑAS
# ============================================================
# Django valida automáticamente que las contraseñas sean seguras
AUTH_PASSWORD_VALIDATORS = [
    # Contraseña no puede ser muy similar al nombre de usuario
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    # Mínimo 8 caracteres
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    # No puede ser una contraseña común (123456, password, etc.)
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    # No puede ser completamente numérica
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ============================================================
# INTERNACIONALIZACIÓN
# ============================================================
LANGUAGE_CODE = 'es-cl'       # Español de Chile
TIME_ZONE = 'America/Santiago' # Zona horaria de Chile
USE_I18N = True                # Habilita traducciones
USE_TZ = True                  # Usa timezone-aware datetimes


# ============================================================
# ARCHIVOS ESTÁTICOS (CSS, JavaScript, Imágenes)
# ============================================================
# URL pública donde se sirven los estáticos
STATIC_URL = '/static/'

# Carpetas donde Django busca archivos estáticos adicionales
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# En producción, collectstatic copia todo aquí
STATIC_ROOT = BASE_DIR / 'staticfiles'


# ============================================================
# REDIRECCIONES DE AUTENTICACIÓN
# ============================================================
# Después de login exitoso, redirige a la lista de clientes
LOGIN_REDIRECT_URL = '/gestion/clientes/'

# Después de logout, redirige al login
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Página de login (usamos la de django.contrib.auth)
LOGIN_URL = '/accounts/login/'


# ============================================================
# TIPO DE CLAVE PRIMARIA POR DEFECTO
# ============================================================
# BigAutoField usa enteros de 64 bits (soporta más registros)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
