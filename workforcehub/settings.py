from pathlib import Path
import os
from employees.get_params import lambda_handler as get_secret

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

secret_params = get_secret()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret_params.get('SECRET_KEY', 'django-insecure-(ezhsmy9s@^(izk18c_z6$9vhupbv+bkp&c)^@a9+hr+u0#lu=')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = secret_params.get('AWS_ALLOWED_HOSTS').split(' ') if secret_params.get('AWS_ALLOWED_HOSTS') else ['localhost', '127.0.0.1']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = secret_params.get('AWS_EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = secret_params.get('AWS_EMAIL_PORT', 587)
EMAIL_USE_TLS = secret_params.get('AWS_EMAIL_USE_TLS', True)
EMAIL_HOST_USER = secret_params.get('AWS_EMAIL_HOST_USER', None)
EMAIL_HOST_PASSWORD = secret_params.get('AWS_EMAIL_HOST_PASSWORD', None)




# configure aws s3 bucket
AWS_STORAGE_BUCKET_NAME = secret_params.get('AWS_STORAGE_BUCKET_NAME')
AWS_ACCESS_KEY_ID = secret_params.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = secret_params.get('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = secret_params.get('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_DEFAULT_ACL = None
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False
AWS_S3_VERIFY = True # Set to False if using a custom domain


AWS_LOCATION = 'media'

INSTALLED_APPS = [
    'employees',
    'organizations',
    'rest_framework',
    'crispy_forms',
    'fontawesomefree',
    "crispy_bootstrap4",
    'storages',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'employees.middleware.ErrorHandlerMiddleware',
    'employees.middleware.NotFoundMiddleware',
    'employees.middleware.Custom404Middleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'workforcehub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'workforcehub.wsgi.application'
USE_L10N = True

# Database
username = secret_params.get('db_username')
password = secret_params.get('db_password')
db_name = secret_params.get('db_name')
host = secret_params.get('db_host')
port = secret_params.get('db_port')

if password and username and db_name and host and port:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': db_name,
            'USER': username,
            'PASSWORD': password,
            'HOST': host,
            'PORT': port,
        }
    }
else:
    DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'workforcehub', 
                'USER': 'kingsley',
                'PASSWORD': 'root',
                'HOST': '',  # wiil evaluate to IP address of the docker container running the database
                'PORT': '5432',    
            }
        }


AUTHENTICATION_BACKENDS = [
    'employees.backends.AdminUserAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# AUTH_MODEL = 'employees.AdminUser'

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

APPEND_SLASH = False

# Settings for Celery   
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Lagos'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
if DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
else:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = '/static/'

# Additional directories where Django should look for static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
LOGIN_URL = 'login'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
