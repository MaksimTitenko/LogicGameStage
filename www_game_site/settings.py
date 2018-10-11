"""
Django settings for www_game_site project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from .site_secret_key import site_key

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = site_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['LogicGameStage.pythonanywhere.com',
                 '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'RoundTable',
    'crispy_forms',
    'mptt',
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

ROOT_URLCONF = 'www_game_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
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

WSGI_APPLICATION = 'www_game_site.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'common_static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Это я подключил чисто для удобного мне отображения формы регистрации и логина
# Установка - pip install django-crispy-forms, можно через настройки интерпретатора
# Потом добавьте это в installed_apps
# Пользуйтесь в шаблонизаторе. Как - увидите в шаблонах login и registration

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Это ссылка на переопределенную модель Юзера в нашем приложении
AUTH_USER_MODEL = 'RoundTable.User'

# Пытаюсь подключить api фейсбука и вконтакте, пока не очень выходит.
# Точнее НЕ входит, вот это каламбур, лол.
# Надо кое-что установить, но опять же, лучше в настройках интерпретатора
# pip install django-mptt>=0.8.7
# pip install facebook - sdk
# pip install vk
#
# Хотя все равно зайти через них не получится


DOMAIN = 'http://127.0.0.1:8000'

VK_APP_ID = '6709264'
VKONTAKTE_APP_ID = VK_APP_ID
VK_API_SECRET = 'wGc02HYDEP0wFOrFh2Xw'
VKONTAKTE_APP_SECRET = VK_API_SECRET

VK_REDIRECT = 'https://oauth.vk.com/authorize?client_id={client_id}&display=page&' \
              'redirect_uri={domain}/vk_callback&scope=email&' \
              'response_type=code&v=5.56&revoke=1'.format(client_id=VK_APP_ID,
                                                          domain=DOMAIN)
VK_URL = 'https://oauth.vk.com/access_token?client_id={client}&' \
         'client_secret={secret}&' \
         'redirect_uri={domain}/vk_callback&' \
         'code='.format(secret=VK_API_SECRET, client=VK_APP_ID, domain=DOMAIN)

FACEBOOK_URL = 'https://graph.facebook.com/v2.7/oauth/access_token?client_id={client_id}&' \
               'client_secret={client_secret}&' \
               'redirect_uri={domain}/facebook_callback/&' \
               'code={code}'

FACEBOOK_APP_ID = '486613158522471'
FACEBOOK_API_SECRET = 'abde6ea5ba503b8dc828a12ac7c626e8'

FACEBOOK_REDIRECT = 'https://www.facebook.com/v2.7/dialog/oauth?' \
                    'client_id={client_id}&redirect_uri={domain}/facebook_callback/' \
    .format(client_id=FACEBOOK_APP_ID, domain=DOMAIN)
