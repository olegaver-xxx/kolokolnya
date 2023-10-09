import django
from pathlib import Path
import os, sys

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = (BASE_DIR/'../data').resolve()
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
SECRET_KEY = os.getenv('SECRET') or 'example'
DEBUG = True

DOMAIN_NAME = os.getenv('DOMAIN_NAME') or 'localhost:8000'
SECURE_CONNECTION = os.getenv('SECURE_CONNECTION', False)
ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.shop',
    'apps.blog',
    'apps.users',
    'easy_thumbnails',
    'bootstrap5',
    'crispy_forms',
    'crispy_bootstrap5',
    'ckeditor'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

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

WSGI_APPLICATION = 'main.wsgi.application'

THUMBNAIL_ALIASES = {
    "": {
        "apps.blog": {'size': (420, 236), 'crop': True},
    },
    "q": {
        "apps.blog": {'size': (1080, 720), 'crop': True},
    },

}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_TZ = True

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
LOGOUT_REDIRECT_URL = '/'

AUTH_USER_MODEL = 'users.User'
STATIC_URL = 'static/'
MEDIA_URL = 'media/'
STATIC_ROOT = DATA_DIR/'static'
MEDIA_ROOT = DATA_DIR/'media'
STATICFILES_DIRS = [
    BASE_DIR/'static'
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
# CKEDITOR_CONFIGS = {
#     'awesome_ckeditor': {
#         'toolbar': 'Basic',
#     },
# }