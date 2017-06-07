from __future__ import absolute_import, unicode_literals

from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qlu!zhydzekoar&^5+-3jz@7gk+skxora)2ds(56j2&+go)!b='


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Minecraft server
MINECRAFT_SERVER_URL = "10.1.1.10"
MINECRAFT_WHITELIST_LOCATION = "whitelist.json"

# Wagtail settings
WAGTAIL_SITE_NAME = "MineDash"

# Base URL to use when referring to full URLs within the Wagtail admin backend
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://localhost:8000'


# Recaptcha settings
RECAPTCHA_PUBLIC_KEY = ""
RECAPTCHA_PRIVATE_KEY = ""

RECAPTCHA_USE_SSL = True
NOCAPTCHA = True
