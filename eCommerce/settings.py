from django.contrib.messages import constants as messages
from pathlib import Path

import environ
# import os

# CURRENCY = os.getenv("CURRENCY", "USD")

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

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
    'accounts',
    'category',
    'store',
    'carts',
    'orders',
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

ROOT_URLCONF = 'eCommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'carts.context_processors.counter'
            ],
        },
    },
]

WSGI_APPLICATION = 'eCommerce.wsgi.application'

# Inform about using `accounts` instead of the default user model
AUTH_USER_MODEL = 'accounts.Account'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env('DATABASE_ENGINE'),
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = env('LANGUAGE_CODE')

TIME_ZONE = env('TIME_ZONE')

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
    'eCommerce/static'
]

# Cầu hình media file
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.WARNING: 'warning',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.DEBUG: 'secondary',
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_USE_TLS = True
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_PORT = env("EMAIL_PORT")