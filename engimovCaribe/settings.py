"""
Django settings for engimovCaribe project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import datetime
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-btr7+_f$(v@!04+gh7wx3wgo5lgwl794uaa2hbs6p3*%bypx84'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True
from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = [*default_headers, 'currency', 'cookie', 'Access-Control-Allow-Origin',
                      'accept-encoding', 'dnt', 'origin', 'Cart-Id']

CORS_EXPOSE_HEADERS = ['currency', 'cookie', 'Cart-Id']
CORS_ORIGIN_WHITELIST = [
    'http://localhost:4200',  # Dominio de tu aplicación Angular
    'https://*.vercel.app',
]
CSRF_TRUSTED_ORIGINS = ['https://*.127.0.0.1', 'https://*.render.com', 'https://*.onrender.com',
                        'http://localhost:4200', 'https://*.vercel.app']
CORS_ALLOW_PRIVATE_NETWORK = True

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sslserver',
    'core.apps.CoreConfig',
    'sections.apps.SectionsConfig',
    'app_cart',
    # third party apps
    'django_q',
    'django_cleanup',
    'rest_framework',
    'drf_yasg',
    'corsheaders',
    'ckeditor',
    'ckeditor_uploader',
    'solo.apps.SoloAppConfig',
]

BUSINESS_LOGO_PATH = 'admin/img/engi_logo.png'
BUSINESS_NAME = 'Admin'
BUSINESS_NAME_IMG_PATH = 'admin/img/engi_logo_2.png'
BUSINESS_BANNER = 'admin/img/banner_lg.png'
BUSINESS_ICON_PATH = 'admin/img/icon_yellow.png'

JAZZMIN_SETTINGS = {
    "site_brand": BUSINESS_NAME,
    "site_title": "Engimov Admin",
    "welcome_sign": '',
    'site_icon': 'vendor/adminlte/img/AdminLTELogo.png',
    'site_logo': BUSINESS_LOGO_PATH,
    'site_logo_classes': 'brand-image',
    "login_logo": BUSINESS_NAME_IMG_PATH,
    "login_logo_dark": BUSINESS_LOGO_PATH,
    'site_header': BUSINESS_NAME,
    "custom_css": 'admin/css/admin.css',
    'copyright': '',
    "order_with_respect_to": ["core", 'sections', 'core.enterprisedata', 'core.ProductCategory', 'core.product',
                              'core.WorkCategory', 'core.work', 'core.JobOffer', 'core.JobOfferPool',
                              'core.CommercialJobOffer'],
}

CKEDITOR_CONFIGS = {
    'default': {
        "skin": "moono-lisa",
        "toolbar_Basic": [["Source", "-", "Bold", "Italic"]],
        "toolbar_Full": [
            [
                "Styles",
                "Format",
                "Bold",
                "Italic",
                "Underline",
                "Strike",
                "SpellChecker",
                "Undo",
                "Redo",
            ],
            ["Link", "Unlink", "Anchor"],
            ["Image", "Flash", "Table", "HorizontalRule"],
            ["TextColor", "BGColor"],
            ["Smiley", "SpecialChar"],
        ],
        "toolbar": "Full",
        "height": 300,
        "width": 'auto',
        "filebrowserWindowWidth": 940,
        "filebrowserWindowHeight": 725,
    }
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'engimovCaribe.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'engimovCaribe.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'engimov',
#         'USER': 'blinit10', #USE YOUR OWN USERNAME
#         'PASSWORD': 'rootzenBL*123', #USE YOUR OWN PASSWORD
#         'HOST': 'localhost',
#         'PORT': '3308',
#         'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'database/db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': 'memchached:11211',
        # We are using here the capabilities of docker dns, when using docker compose up the service name it resolves to is docker ip
    },
    'local': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

# LANGUAGE_CODE = 'pt-br'
# LANGUAGES = [('pt-br', 'Português'), ('es', 'Español')]
LANGUAGE_CODE = 'es'
LOCALE_PATHS = (str(BASE_DIR / 'locale'),)

TIME_ZONE = 'America/Havana'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '208.118.63.250'
EMAIL_HOST_USER = 'reservas@casa7ma.com'
EMAIL_HOST_PASSWORD = 'FrutaBomba2023..'  # past the key or password app here
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# DJANGO QUEUE
Q_CLUSTER = {
    'name': 'DjangORM',
    'workers': 4,
    'timeout': 43200,
    'retry': (43200 * 2),
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default'
}

# DJANGO SOLO
SOLO_ADMIN_SKIP_OBJECT_LIST_PAGE = True
SOLO_CACHE_TIMEOUT = 60 * 5  # 5 mins
SOLO_CACHE = 'local'
SOLO_CACHE_PREFIX = 'solo'
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

CKEDITOR_UPLOAD_PATH = "richdata/"
CKEDITOR_CONFIGS = {
    'default': {
        "skin": "moono-lisa",
        "toolbar_Basic": [["Source", "-", "Bold", "Italic"]],
        "toolbar_Full": [
            [
                "Styles",
                "Format",
                "Bold",
                "Italic",
                "Underline",
                "Strike",
                "SpellChecker",
                "Undo",
                "Redo",
            ],
            ["Link", "Unlink", "Anchor"],
            ["Image", "Flash", "Table", "HorizontalRule"],
            ["TextColor", "BGColor"],
            ["Smiley", "SpecialChar"],
        ],
        "toolbar": "Full",
        "height": 150,
        "width": 500,
        "filebrowserWindowWidth": 940,
        "filebrowserWindowHeight": 725,
    }
}
CART_SESSION_ID = "cart"
SESSION_COOKIE_AGE = 7200

TPP_CLIENT_ID = 'f12538a0aa85242baa9f137380ab1926'
TPP_CLIENT_SECRET = '323b25d45c305000cec8c8a70afc4cda'
TPP_CLIENT_EMAIL = 'gaia.habana2021@gmail.com'
TPP_CLIENT_PASSWORD = 'Gaia2021'
TPP_URL = "www.tropipay.com"
TPP_SUCCESS_URL = 'https://gaia-mercado.com/tropipay/success/'
TPP_FAILED_URL = 'https://gaia-mercado.com/tropipay/fails/'
TPP_NOTIFICACION_URL = 'https://gaia-mercado.com/tropipay/verificar/'
