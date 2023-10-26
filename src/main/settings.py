import django
from pathlib import Path
import os, sys

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = (BASE_DIR/'../data').resolve()
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
SECRET_KEY = os.getenv('SECRET') or 'example'
DEBUG = bool(os.getenv('DEBUG'))

DOMAIN_NAME = os.getenv('DOMAIN_NAME') or 'localhost:8000'
SECURE_CONNECTION = os.getenv('SECURE_CONNECTION', False)
PROTOCOL = 'https://' if SECURE_CONNECTION else 'http://'
ALLOWED_HOSTS = ["localhost"]


INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'yookassa',
    'apps.shop',
    'apps.blog',
    'apps.users',
    'apps.utils',
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
                'apps.utils.context_processor.get_site_prefs',
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
if os.getenv('POSTGRES_HOST'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('POSTGRES_DB') or 'kolo_db',
            'USER': os.getenv('POSTGRES_USER') or 'admin',
            'PASSWORD': os.getenv('POSTGRES_PASSWORD') or 'admin',
            'HOST': os.getenv('POSTGRES_HOST') or 'localhost',
            'PORT': int(os.getenv('POSTGRES_PORT', 0)) or 5432,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': DATA_DIR / 'db.sqlite3',
        }
    }

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
if DEBUG:
    AUTH_PASSWORD_VALIDATORS = []

# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_TZ = True

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/profile/'
AUTH_USER_MODEL = 'users.User'
STATIC_URL = 'static/'
MEDIA_URL = 'media/'

MEDIA_ROOT = DATA_DIR/'media'
STATICFILES_DIRS = [
    BASE_DIR/'static'
]
STATIC_ROOT = DATA_DIR/'static'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
# CKEDITOR_CONFIGS = {
#     'awesome_ckeditor': {
#         'toolbar': 'Basic',
#     },
# }

JAZZMIN_SETTINGS = {
    # title of the window
    "site_title": os.getenv('SITE_TITLE') or "Колокольня",

    # Title on the brand, and the login screen (19 chars max)
    "site_header": os.getenv('SITE_TITLE') or "Колокольня",

    'site_brand': os.getenv('SITE_TITLE') or 'Колокольня',

    # square logo to use for your site, must be present in static files, used for favicon and brand on top left
    "site_logo": os.getenv('SITE_LOGO') or 'images/logo.png',
    "site_icon": None,

    # Welcome text on the login screen
    "welcome_sign": "Welcome to the Kolololnya",

    # Copyright on the footer
    "copyright": "Oleg",

    # The model admin to search from the search bar, search bar omitted if excluded
    # "search_model": "core.SGUser",

    # Field name on user model that contains avatar image
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [
        # {"name": "Index", 'url': 'index'},

        # Url that gets reversed (Permissions can be added)
        {"name": "View Site",  "url": "home", "permissions": []},
        {"name": "Preferences",  "url": "admin_prefs", "permissions": []},

    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    # "usermenu_links": [
    #     {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
    #     # {"model": "auth.user"}
    # ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ['auth', 'users'],

    # Custom links to append to app groups, keyed on app name
    # "custom_links": {
    #     "shortcuts": [{
    #         "name": "Preferences2",
    #         "url": "index",
    #         "icon": "fas fa-comments",
    #         # "permissions": ["books.view_book"]
    #     }]
    # },

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free
    # for a list of icon classes
    "icons": {
        "users.UserModel": "fas fa-user",
        # "sguser.Settings": "fas fa-user-cog",
        "auth.Group": "fas fa-users-cog",
        # "auth.Group": "fas fa-users",
        "auth.Permission": "fas fa-user-lock",

    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": "css/custom_admin.css",
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "vertical_tabs",
    # override change forms on a per modeladmin basis
    # "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs",},
    # Add a language dropdown into the admin
    "language_chooser": False,

}

YOOKASSA_API_KEY = os.getenv('YOOKASSA_API_KEY')
YOOKASSA_SHOP_ID = os.getenv('YOOKASSA_SHOP_ID')
# from yookassa import Configuration
