import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


SECRET_KEY = '^yz(wrfzsrq5x2(ee(@6rab3s8r2(h1a(92wmzf7hta8hdxf0u'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
