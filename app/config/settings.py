"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
import config.db as db

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

""" Comments 
    #Concatena la ruta base con templates.
    os.path.join(BASE_DIR,'templates')

"""

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_&ig-9zewpb8!lw#ov_o8sa1q0ggoydlj&y$)9&)*cer5+qbl0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_seed',
    'widget_tweaks',
    # apps
    'core.erp',
    'core.homepage',
    'core.login',
    'core.user',
    'core.reports',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'crum.CurrentRequestUserMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = db.SQLITE

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
"""Cuando ejecutamos COLLECTSTATIC para poner todos los archivos
estaticos en una sola carpetatenemos que definir a que carpeta iran esos archivos en STATIC_ROOT"""
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/') #BASE_DIR obtencion de la ruta del directorio

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -- login config
LOGIN_REDIRECT_URL = '/erp/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'

# en caso de un PageNotFound que redirija al login
LOGIN_URL = '/login/'

# media config
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'user.User'

""" En las sesiones no se pueden serializar los objetos (En este caso instancias de modelos) para poder
 pasar datos a las sesiones (request.session['group'] = Group.objects.get(pk=self.kwargs['pk']))
  debemos cambiar el SESSION_SERIALIZER para que no se serialize como un JSON.
  Esto nos permitira trabajar con objetos dentro de las sesiones"""
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

#EMAIL CONFIG

#servidor SMTP
EMAIL_HOST = 'smtp.gmail.com'
#puerto del host
EMAIL_PORT = 587
EMAIL_HOST_USER = 'horusdevmail@gmail.com'
EMAIL_HOST_PASSWORD = 'qdqvvuukobwxkzqo'

DOMAIN = ''