import os
from pathlib import Path
import dj_database_url

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# SEGURIDAD: Llave secreta
SECRET_KEY = os.environ.get('SECRET_KEY', default='django-insecure-examen-jean-pierre-2026')

# DEBUG: Falso en Render, Verdadero en local
DEBUG = 'RENDER' not in os.environ

# CORRECCIÓN VITAL: Permitir todos los hosts en Render para evitar Error 500
ALLOWED_HOSTS = ['*']

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks', # Tu aplicación principal
]

# Middleware optimizado (WhiteNoise corregido)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Sirve archivos estáticos en Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangocrud.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media', # VITAL para las fotos de Venta Garage
            ],
        },
    },
]

WSGI_APPLICATION = 'djangocrud.wsgi.application'

# Base de datos: Soporta SQLite local y PostgreSQL en Render automáticamente
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

# Validadores de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalización (Configurado para Ecuador)
LANGUAGE_CODE = 'es-ec'
TIME_ZONE = 'America/Guayaquil'
USE_I18N = True
USE_TZ = True

# Archivos Estáticos (CSS, JS)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# CORRECCIÓN VITAL: Evita que el servidor explote si falta un archivo estático
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Archivos Media (Fotos de Perfil y Venta Garage)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Redirecciones
LOGIN_URL = '/signin'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/signin'

# CORRECCIÓN VITAL: Para que Render acepte los formularios (Login/Signup)
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'