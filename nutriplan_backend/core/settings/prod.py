from .base import *

import environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True),
    POSTGRESQL_NAME = ('raliway'),
    POSTGRESQL_USER = ('postgres'),
    POSTGRESQL_PASS = ('fxHWHFBOh4rCS55FerQD'),
    POSTGRESQL_HOST = ('containers-us-west-122.railway.app'),
    POSTGRESQL_PORT = ('7760')
)
# reading .env file
environ.Env.read_env()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('POSTGRESQL_NAME'),
        'USER': env('POSTGRESQL_USER'),
        'PASSWORD': env('POSTGRESQL_PASS'),
        'HOST': env('POSTGRESQL_HOST'),
        'PORT': env('POSTGRESQL_PORT'),
    }
}
