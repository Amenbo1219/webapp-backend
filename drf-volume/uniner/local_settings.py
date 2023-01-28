from .settings import *
import environ
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env()

environ.Env.read_env(os.path.join(BASE_DIR, 'docker.env'))
DEBUG = True
ALLOWED_HOSTS = [env('POSTGRES_HOST')]
SECRET_KEY = env('SECRET_KEY')
CORS_ORIGIN_WHITELIST = [
    'http://localhost'
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    }
}
