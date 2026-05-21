from pathlib import Path
import os
from dotenv import load_dotenv  # Kaliya kani baa ku filan

# Jidka (Path) asaasiga ah ee mashruuca
BASE_DIR = Path(__file__).resolve().parent.parent

# Soo rurinta feylka .env ee sirta ah
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Ammaanka Furayaasha (Waxaa laga soo akhrinayaa .env)
# Waxaa lagu daray furihii hore oo ammaan u ah fallback haddii .env la waayo waqti tijaabo ah
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-moxamed-samee-app-builder-project-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS - Waxaa lagu daray domains-ka aad ku kalsoon tahay ee ku jiray CSRF
ALLOWED_HOSTS = [
    'maxamed.serveo.net', 
    'maxamed.serveousercontent.com', 
    'maxamed.up.railway.app',                      # Loo baahan yahay Railway
    'facebook-cranial-crabbing.ngrok-free.dev',    # Loo baahan yahay Ngrok
    '127.0.0.1', 
    'localhost'
]

# Apps-ka rakiban
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
    'import_export', 
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',  # Nidaamka Session-ka (Loo baahan yahay)
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Nidaamka aqoonsiga User-ka (Halkan ayuu ku dhalanayaa)
    
    # 🔥 HALKAN DHIG: Hadda request.user si nabad ah ayuu u shaqaynayaa
    'core.middleware.MaintenanceMiddleware', 
    
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

# Database (PostgreSQL) - Waxaa gabi ahaanba loo wareejiyay .env dynamic config
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'AppBuilderProject'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD'), 
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '5432'),
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

# --- HABAYNTA IMPORT-EXPORT (CILAD-BIXINTA UNICODE) ---
IMPORT_EXPORT_USE_TRANSACTIONS = True
IMPORT_EXPORT_SKIP_ADMIN_LOG = True
IMPORT_EXPORT_ENCODING = 'utf-8-sig'