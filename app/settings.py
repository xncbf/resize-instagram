LANGUAGE_CODE = 'ko'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

AWS_S3_BUCKET_NAME_STATIC = "resize-static"

AWS_S3_CUSTOM_DOMAIN = 'resize-static.s3.amazonaws.com'
STATIC_URL = "https://resize-static.s3.amazonaws.com/"

AWS_S3_BUCKET_NAME_MEDIA = "resize-media"

PWA_APP_NAME = 'Resize'
PWA_APP_DESCRIPTION = "Resize for instagram"
PWA_APP_THEME_COLOR = '#de91ff'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone' # fullscreen
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_ICONS = [
    {
        'src': STATIC_URL + 'icon-160x160.png',
        'sizes': '160x160'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': STATIC_URL + 'icon-160x160.png',
        'sizes': '160x160'
    }
]
PWA_APP_SPLASH_SCREEN = [
    # {
    #     'src': STATIC_URL + 'resize-instagram2.png', # 640x1136
    #     'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    # }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'
PWA_APP_DEBUG_MODE = DEBUG
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'app', 'serviceworker.js')
