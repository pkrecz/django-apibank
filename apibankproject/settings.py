# -*- coding: utf-8 -*-

import os
import dj_database_url
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', default=False)
ALLOWED_HOSTS = list(os.getenv('ALLOWED_HOSTS').split(' '))


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apibankapp',
    'rest_framework',
    'django_filters',
    'rest_framework.authtoken',
    'drf_yasg',]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apibankapp.middleware.ExceptionMiddleware',]


ROOT_URLCONF = 'apibankproject.urls'


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
                'django.contrib.messages.context_processors.messages',],
        },
    },
]

WSGI_APPLICATION = 'apibankproject.wsgi.application'


DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL_LOCAL'))}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},]


# Internationalization
LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / str(os.getenv('STATIC_ROOT'))
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/'),]


# Media settings
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / str(os.getenv('MEDIA_ROOT'))


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Restframework settings
REST_FRAMEWORK = {

    'DATE_INPUT_FORMATS': ['%Y-%m-%d',],
    'DATE_FORMAT': '%Y-%m-%d',
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',],
    
    'DEFAULT_PAGINATION_CLASS': 'apibankapp.paginations.CustomLimitOffsetPagination',

    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',],
    
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',],
}
