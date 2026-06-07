import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url  # 🔥 Loogu talogalay inuu Koyeb si toos ah u xiriiriyo Database-ka

# Jidka (Path) asaasiga ah ee mashruuca
BASE_DIR = Path(__file__).resolve().parent.parent

# Soo rurinta feylka .env ee sirta ah
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Ammaanka Furayaasha (Waxaa laga soo akhrinayaa .env)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-change-this-in-production')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# 🔥 ALLOWED_HOSTS - Waxaa lagu daray cinwaanka Koyeb ee cusub
ALLOWED_HOSTS = [
    'maxamed.serveo.net', 
    'maxamed.serveousercontent.com', 
    '127.0.0.1', 
    'localhost',
    '172.21.253.103',
    '.koyeb.app',      # 🔥 Waxay si toos ah u ogolaanaysaa link kasta oo Koyeb kuu siiyo
    '*'                # 🔥 Waxay oggolaanaysaa aalad kasta (aad u muhiim u ah Mobile-ka)
]

# ---------------------------------------------------
# 🔥 APPS-KA RAKIBAN (INSTALLED APPS)
# ---------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'import_export', 
    
    'maxamed_game',
    'maxamed_Ai',
    'keep_notes',
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
    'maintenance', 
    'my_messages',
    'poll',
    'profile_html', 
    'quiz',
    'register',
    'result',
    'tts_interface',
]

# ---------------------------------------------------
# 🔥 MIDDLEWARE (WhiteNoise ayaa static-ka online ka dhigaya)
# ---------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # 🔥 Maareynta static-ka ee server-ka
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

# ---------------------------------------------------
# 🔥 DATABASE CONFIGURATION (U DIYAAR INTANETKA)
# ---------------------------------------------------
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

# 🔥 Haddii uu koodhku joogo Koyeb, si toos ah u isticmaal Database-ka server-ka bilaashka ah
if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)


# ---------------------------------------------------
# 🔥 STATIC & MEDIA FILES (Maareynta Offline-ka iyo PWA)
# ---------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# WhiteNoise storage ee koodhka adkeeya
STATICFILES_STORAGE = 'whitename_disabled_for_pwa' # Waxaan u dhaafnay mid dabiici ah si uu PWA u kaydiyo
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

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

# ---------------------------------------------------
# 🔥 CSRF_TRUSTED_ORIGINS (Loo safeeyay badbaadadaada)
# ---------------------------------------------------
CSRF_TRUSTED_ORIGINS = [
    'https://maxamed.serveo.net',
    'https://maxamed.serveousercontent.com',
    'https://*.serveo.net',
    'https://*.serveousercontent.com',
    'https://*.koyeb.app',  # 🔥 Waxay ogolaanaysaa link kasta oo Koyeb kuu siiyo rasmiga ah
    'https://facebook-cranial-crabbing.ngrok-free.dev',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- HABAYNTA IMPORT-EXPORT ---
IMPORT_EXPORT_USE_TRANSACTIONS = True
IMPORT_EXPORT_SKIP_ADMIN_LOG = True
IMPORT_EXPORT_ENCODING = 'utf-8-sig'