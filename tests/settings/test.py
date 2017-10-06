from .common import *  # noqa


INVITE_SHOW_EMAILS = True

INVITE_OPEN_INVITE_CUTOFF = 1

INVITE_REGISTRATION_CUTOFF = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
