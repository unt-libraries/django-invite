from .common import *  # noqa

INVITE_SHOW_EMAILS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),   # noqa: F405
    }
}
