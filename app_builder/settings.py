import os
from pathlib import Path
from dotenv import load_dotenv

# Jidka (Path) asaasiga ah ee mashruuca
BASE_DIR = Path(__file__).resolve().parent.parent

# Soo rurinta feylka .env ee sirta ah
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Ammaanka Furayaasha (Waxaa laga soo akhrinayaa .env)
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS
ALLOWED_HOSTS = [
    'maxamed.serveo.net', 
    'maxamed.serveousercontent.com', 
    '127.0.0.1', 
    'localhost'
]

# ---------------------------------------------------
# 🔥 APPS-KA RAKIBAN (INSTALLED APPS)
# ---------------------------------------------------
INSTALLED_APPS = [
    # Apps-ka rasmiga ah ee Django la yimaado
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Packages-ka dibadda ka yimid (Third-party apps)
    'import_export', 
    
    # 20-ka Apps ee cusub ee go'doonka ah ee aad sameysay
    'about',
    'app_detail',
    'banaadir',
    'chat_window',
    'chats',
    'contact',
    'content',
    'create_app',
    'dashboard',
    'editor',
    'homepage',
    'login',
    'maintenance',  # App-ka maintenance halkan ayuu si toos ah u joogaa
    'my_messages',
    'poll',
    'profile_html',  # App-kii profile-ka ee badbaadada ahaa
    'quiz',
    'register',
    'result',
    'tts_interface',
]

# ---------------------------------------------------
# 🔥 MIDDLEWARE (Halkan waxaa la geliyay jidka saxda ah)
# ---------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Jidka cusub ee rasmiga ah ee Middleware-kaaga Maintenance-ka:
    'maintenance.middleware.MaintenanceMiddleware',
]

ROOT_URLCONF = 'app_builder.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app_builder.wsgi.application'

# Database (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'AppBuilderProject',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('DB_PASSWORD'), 
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_uploads')

# Login/Logout Settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# Session Settings
SESSION_COOKIE_AGE = 60 * 60 * 24 * 365 
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True

# CSRF_TRUSTED_ORIGINS
CSRF_TRUSTED_ORIGINS = [
    'https://maxamed.serveo.net',
    'https://maxamed.serveousercontent.com',
    'https://*.serveo.net',
    'https://*.serveousercontent.com',
    'https://maxamed.up.railway.app',
    'https://facebook-cranial-crabbing.ngrok-free.dev',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- HABAYNTA IMPORT-EXPORT ---
IMPORT_EXPORT_USE_TRANSACTIONS = True
IMPORT_EXPORT_SKIP_ADMIN_LOG = True
IMPORT_EXPORT_ENCODING = 'utf-8-sig'