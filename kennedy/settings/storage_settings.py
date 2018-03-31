"""Settings related to file handling"""
# pylint: disable=invalid-name
import os

from boto.s3.connection import OrdinaryCallingFormat
import environ

env = environ.Env(
    DEBUG=(bool, False),
    USE_S3=(bool, False),
    DEFAULT_S3_PATH=(str, 'kennedy/uploads'),
    STATIC_S3_PATH=(str, 'kennedy/static')
)


BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))


# Locations of static assets
STATICFILES_DIRS = (
    os.path.join(BASE_PATH, 'dist'),
)

# Preload metadata for S3 (used for django-s3-collectstatic)
AWS_PRELOAD_METADATA = True

# Test of we should be using S3 for static files or fall back to filesystem
# storage
if env('USE_S3'):
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')

    # If you're using a custom domain other than `bucketname.s3.amazonaws.com`
    # assign it to `AWS_S3_CUSTOM_DOMAIN`
    # This will be used for static assets only, as our storage engine does
    # not support secure URLs not hosted on S3.
    # THIS DOMAIN MUST HAVE A VALID SSL CERTIFICATE
    AWS_S3_CUSTOM_DOMAIN = env(
        'AWS_S3_CUSTOM_DOMAIN',
        default='%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME)

    AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()

    STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
    DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
    ATTACHMENT_STORAGE_ENGINE = DEFAULT_FILE_STORAGE

    # Paths on S3 for various content
    DEFAULT_S3_PATH = env('DEFAULT_S3_PATH')
    STATIC_S3_PATH = env('STATIC_S3_PATH')

    STATIC_ROOT = "/%s/" % STATIC_S3_PATH
    STATIC_URL = '//%s/%s/' % (
        AWS_S3_CUSTOM_DOMAIN, STATIC_S3_PATH)
    AWS_DEFAULT_ACL = 'public-read'

    MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
    MEDIA_URL = '//%s/%s/' % (
        AWS_S3_CUSTOM_DOMAIN, DEFAULT_S3_PATH)

else:
    MEDIA_ROOT = os.path.join(BASE_PATH, 'uploads')
    MEDIA_URL = '/uploads/'
    STATIC_ROOT = os.path.join(BASE_PATH, 'static')
    STATIC_URL = '/static/'

    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    ATTACHMENT_STORAGE_ENGINE = DEFAULT_FILE_STORAGE
