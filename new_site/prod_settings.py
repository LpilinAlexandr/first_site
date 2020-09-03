import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


SECRET_KEY = '^yz(wrfzsrq5x2(ee(@6agfvasdgvas(h1a(92wmzf7hta8hdxf0u'

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'shop',
        'USER': 'postgres',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')