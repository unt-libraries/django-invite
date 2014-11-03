from django.conf import settings
from django.core.urlresolvers import reverse_lazy


INVITE_LOGOUT_REDIRECT_URL = getattr(
    settings,
    'INVITE_LOGOUT_REDIRECT_URL',
    reverse_lazy('invite:index')
)

INVITE_SIGNUP_REDIRECT_PATH = getattr(
    settings,
    'INVITE_SIGNUP_REDIRECT_PATH',
    reverse_lazy('invite:index')
)

INVITE_SERVICE_NAME = getattr(
    settings,
    'INVITE_SERVICE_NAME',
    'Invite App App'
)

INVITE_DEFAULT_FROM_EMAIL = getattr(
    settings,
    'INVITE_DEFAULT_FROM_EMAIL',
    settings.DEFAULT_FROM_EMAIL
)

