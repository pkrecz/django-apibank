# -*- coding: utf-8 -*-

import os
import dj_database_url
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', default=False)
ALLOWED_HOSTS = list(os.getenv('ALLOWED_HOSTS').split(' '))


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
    'drf_yasg',
    'debug_toolbar']


MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apibankapp.middleware.ExceptionMiddleware',]


CACHE_MIDDLEWARE_SECONDS = 120
CACHE_MIDDLEWARE_KEY_PREFIX = ''


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
    },]


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


CACHES = {
            'default': {
                            'BACKEND': 'django_redis.cache.RedisCache',
                            'LOCATION': os.getenv('REDIS_URL', default='redis://127.0.0.1:6379/'),
                            'OPTIONS': {
                                            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                                            'CONNECTION_POOL_KWARGS': {
                                                                        'max_connections': 100,
                                                                        'retry_on_timeout': True}
                                        }
                        }
        }


SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'


LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / str(os.getenv('STATIC_ROOT'))
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/'),]


MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / str(os.getenv('MEDIA_ROOT'))


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


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
        'rest_framework.renderers.JSONRenderer',],}


SWAGGER_SETTINGS = {
    "DEFAULT_AUTO_SCHEMA_CLASS": "apibankapp.custom.CustomAutoSchema"}


DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.alerts.AlertsPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',]


DEBUG_TOOLBAR_CONFIG = {
    'RESULTS_CACHE_SIZE': 1000,
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
    'RENDER_PANELS': False}
