import datetime
import os

AWS_GROUP_NAME = "Noubar-Ecommerce-Group"
AWS_USERNAME = "noubar-ecommerce-user"
# the lines above is only for reference not to be used for access
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID","AKIAJYKT2MVMTXPDDZXQ")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY","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")

AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False

DEFAULT_FILE_STORAGE = 'PythonEcommerceProject.aws.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'PythonEcommerceProject.aws.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'noubar-ecommerce'
S3DIRECT_REGION = 'us-east-1'
S3_URL = '//s3-%s.amazonaws.com/%s' % (S3DIRECT_REGION ,AWS_STORAGE_BUCKET_NAME)
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = {
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}

PROTECTED_DIR_NAME = 'protected'
PROTECTED_MEDIA_URL = '//s3-%s.amazonaws.com/%s/%s' %(S3DIRECT_REGION, AWS_STORAGE_BUCKET_NAME, PROTECTED_DIR_NAME)

AWS_DOWNLOAD_EXPIRE = 5000 #(0ptional, in milliseconds)
