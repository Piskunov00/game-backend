import os
from .settings import *


DB_ENGINE = os.getenv('ENGINE') or 'django.db.backends.postgresql'
DB_NAME = os.getenv('NAME') or 'ifrag'
DB_USER = os.getenv('USER') or 'ifrag'
DB_PASSWORD = os.getenv('PASSWORD') or 'ifrag'
DB_HOST = os.getenv('HOST') or 'database'
DB_PORT = int(os.getenv('PORT') or '5432')

DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}
