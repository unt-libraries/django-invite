from .common import *  # noqa

INVITE_SHOW_EMAILS = True

INVITE_OPEN_INVITE_CUTOFF = 90

INVITE_REGISTRATION_CUTOFF = 90

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),   # noqa: F405
    }
}
