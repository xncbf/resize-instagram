LANGUAGE_CODE = 'ko'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

AWS_S3_BUCKET_NAME_STATIC = "resize-static"

AWS_S3_CUSTOM_DOMAIN = 'resize-static.s3.amazonaws.com'
STATIC_URL = "https://resize-static.s3.amazonaws.com/"

AWS_S3_BUCKET_NAME_MEDIA = "resize-media"

