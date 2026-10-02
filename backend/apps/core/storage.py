from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class PublicMediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    default_acl = None
    querystring_auth = False


class PrivateMediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_PRIVATE_BUCKET_NAME or settings.AWS_STORAGE_BUCKET_NAME
    default_acl = None
    querystring_auth = True
    querystring_expire = 300

