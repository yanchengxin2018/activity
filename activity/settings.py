import os,datetime

# from main.tools import my_exception_handle
# REST_FRAMEWORK = {
# 'EXCEPTION_HANDLER':my_exception_handle
# }
#抽奖者标准
SUPPORTERCOUNT=1
STARTPASSWORD='147852369'
# ROOR_IP='http://172.16.10.132:8009'
ROOR_IP='http://180.76.163.21:8888'


TRIESLIMIT=3  #ip限制次数,废弃的
LIMITEDTIME=datetime.timedelta(minutes=0,seconds=1)   #ip限制时间，废弃的
CODE_USER='QT-yybb'        #短信模块的用户名
CODE_PASSWORD='Net263yy'   #短信模块的密码
# CODE_TEST=True             #短信模块当前是不是测试模式,如果是True,则不会真的发送，而是打印在终端
CODE_TEST=False

# DEBUG = True
DEBUG = False
CODE_TIME=datetime.timedelta(minutes=1) #短信验证码限制发送时间

CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:8000',
    'localhost:8000',
)
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Authorization',
    'async',
    'process-Data',
)
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL=True


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = '$&te!o#*e9k!l+=_on9ai2+5d%^+rbtevcszpaff-xh01c85k9'

ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #应用
    'main',

    # 依赖
    'django_extensions',
    'rest_framework',
    'rest_framework_swagger',
    'django_filters',
    'corsheaders',

]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', #cors通过
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'activity.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'activity.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

# USE_TZ = True
USE_TZ = False

STATIC_URL = '/image_dir/'
STATIC_ROOT=os.path.join(BASE_DIR, 'image_dir')
# STATICFILES_DIRS=[os.path.join(BASE_DIR+'/image_dir/')]


# os.path.join(os.path.dirname(__file__), '../static/').replace('\\','/'),










