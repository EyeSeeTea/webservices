import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'in##hj=!8!%v+%i0f!9a(#eq^bgc6lnz^lkt%rkgql*0=2tm&^'
DEBUG = True

ALLOWED_HOSTS = [
    "django-reverse-proxy.herokuapp.com",
    "127.0.0.1",
    "localhost",
]

INSTALLED_APPS = [
    'revproxy',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'webservices.urls'
WSGI_APPLICATION = 'webservices.wsgi.application'
TARGET = "http://scipion.i2pc.es"
