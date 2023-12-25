"""
Django settings for djangoProject1 project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.contrib.auth.decorators import permission_required
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@j-1tiq463#h4t5jm295f#-z(icpua+qpj*p51+6bzs^dh-^q!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
firebaseConfig = {
      "apiKey": "AIzaSyCiFOxhd2Q5lApWM_Q2t7YH69AwK-X2P6k",
      "authDomain": "oorthoschools.firebaseapp.com",
      "projectId": "oorthoschools",
      "storageBucket": "oorthoschools.appspot.com",
      "messagingSenderId": "266788630014",
      "appId": "1:266788630014:web:8c1a4e24cb80c17ee4a4af",
      "measurementId": "G-FWLKR2ZNC2"
}
SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, 'common_static', 'css')
SASS_PROCESSOR_INCLUDE_DIRS = [
    os.path.join(BASE_DIR, 'common_static', 'css'),
    # Include app-specific SCSS directories under the 'css' folder
    # Add any other SCSS include directories here
]

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'
# ADMIN_TOOLS_INDEX_DASHBOARD = 'blog.dashboard.CustomDashboard'


DJOSER = {
    'LOGIN_FIELD': "email",
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,
    'SERIALIZERS': {
        'user_create': 'useraccount.api.serializers.user_api_serializer.RegisterRequestSerializer',
        # your serializer
    }

}
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'mail.orthoschools.com'
EMAIL_HOST_USER = 'auth@orthoschools.com'
EMAIL_HOST_PASSWORD = 'Java456!@'
EMAIL_PORT = 587
# EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'auth@orthoschools.com'

INSTALLED_APPS = ["admin_confirm",

                  "unfold",  # before django.contrib.admin
                  "unfold.contrib.filters",  # optional, if special filters are needed
                  "unfold.contrib.forms",  # optional, if special form elements are needed
                  "unfold.contrib.import_export",  # optional, if django-import-export package is used
                  "unfold.contrib.guardian",  # optional, if django-guardian package is used
                  "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
                  # "django.contrib.admin",  # required

                  # 'django_admin_bootstrapped',
                  # 'admin_tools',
                  # 'admin_tools.dashboard',
                  'django_static_fontawesome',
                  'django_static_jquery3',
                  # 'django_admin_global_sidebar',
                  # 'admin_interface',
                  'colorfield',
                  'widget_tweaks',
                  'django.contrib.admin',
                  'sass_processor',
                  'django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.messages',
                  'django.contrib.staticfiles',
                  'useraccount',
                  'rest_framework',
                  'rest_framework.authtoken',
                  'djoser',
                  'django.contrib.sites',
                  'actstream',                  'core',
                  'drf_spectacular',
                  'space',
                  'blog',
                  'ckeditor',
                  'course',
                  'commentable', 'likable',
                  'django_quill',
                  'notifications'
                  ]
ADMIN_INTERFACE_SETTING = {
    'show_sidebar': False,
    'show_topbar': True,
    'theme': 'flat_responsive',
    'title': 'Your Admin Panel Title',
    'favicon': '/static/admin_interface/img/favicon.ico',
}
SITE_ID = 1

AUTH_USER_MODEL = 'useraccount.UserAccount'
# ACTSTREAM_SETTINGS = {
#     'MANAGER': 'useraccount.managers.MyActionManager',
#     'FETCH_RELATIONS': True,
#     'USE_PREFETCH': True,
#     'USE_JSONFIELD': True,
#     'GFK_FETCH_DEPTH': 1,
# }

# REST_FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# DJOSER


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoProject1.urls'
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.AllowAllUsersModelBackend",
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # Global templates directory
        ],
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

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

WSGI_APPLICATION = 'djangoProject1.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # <-- UPDATED line
        'NAME': 'orthosch_orthoaca',  # <-- UPDATED line
        'USER': 'orthosch_myad',  # <-- UPDATED line
        'PASSWORD': 'Java2992!',  # <-- UPDATED line
        'HOST': '108.61.198.173',  # <-- UPDATED line
        'PORT': '3306',
    }
}
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": "mydatabase",
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static'), ]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py

# Activate internationalization
USE_I18N = True

# Set the languages you want to support
LANGUAGES = [
    ('en', 'English'),
    ('ar', 'Arabic'),
    # Add more languages as needed
]

# Set the default language
LANGUAGE_CODE = 'en'

# Enable localization of dates, numbers, and time
USE_L10N = True

# Specify where Django should store translation files
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),  # Change 'locale' to the directory you choose
]

DJANGO_ADMIN_GLOBAL_SIDEBAR_MENUS = [

    {
        "title": "Home",
        "icon": "fa fa-home",
        "url": "/admin/",
    }, {
        "title": "Manage Books",
        "icon": "fa fa-book",
        "children": [
            {
                "title": "Manage Spaces",
                "icon": "fas fa-list",
                "model": "space.space",
                # "permissions": ["django_admin_global_sidebar_example.view_category"],
            }
        ]
    }, {
        "title": "Authenticate",
        "icon": "fa fa-cogs",
        "children": [

            # {
            #     "title": "Manage Groups",
            #     "icon": "fas fa-users",
            #     "model": "auth.group",
            #     "permissions": ["auth.view_group",],
            # }
        ]
    },
]

UNFOLD = {
    "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
    "SHOW_HEADER": False,  # show/hide header, default: True
    "SIDEBAR": {

        "title": "Orthoaca",
        # "image": "https://www.orthoaca.com/wp-content/uploads/2021/09/Orthoaca-Logo-1.png",
        "show_on_all_pages": True,  # show/hide sidebar on all pages, default: True

        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,
        # Dropdown with all applications and models
        "navigation": [
            {
                # "title": "Navigation",
                # "separator": True,  # Top border
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        # "badge": "sample_app.badge_callback",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Manage Users",
                        "icon": "people",
                        "link": reverse_lazy("admin:useraccount_useraccount_changelist"),
                        # "permission": lambda request: permission_required("useraccount.view_useraccount", raise_exception=False),
                    },
                    {
                        "title": "Manage Spaces",
                        "icon": "diversity_2",
                        "link": reverse_lazy("admin:space_space_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "space.view_space") or request.user.has_perm(
                            "space.change_space") or request.user.is_superuser,
                    },

                    {
                        "title": "Manage Courses",
                        "icon": "school",
                        "link": reverse_lazy("admin:course_course_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "course.view_course") or request.user.has_perm(
                            "course.change_course") or request.user.is_superuser,
                    },

                ],
            },

        ],
    },

    "SHOW_HISTORY": True,  # show/hide "History" button, default: True

    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "fr": "🇫🇷",
                "nl": "🇧🇪",
            },
        },
    },
}
