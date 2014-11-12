from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.contrib.sites.models import Site


INVITE_LOGOUT_REDIRECT_URL = getattr(
    settings,
    'INVITE_LOGOUT_REDIRECT_URL',
    reverse_lazy('invite:index')
)

INVITE_SIGNUP_SUCCESS_URL = getattr(
    settings,
    'INVITE_SIGNUP_REDIRECT_PATH',
    reverse_lazy('invite:index')
)

INVITE_SERVICE_NAME = getattr(
    settings,
    'INVITE_SERVICE_NAME',
    Site.objects.get_current().domain
)

INVITE_DEFAULT_FROM_EMAIL = getattr(
    settings,
    'INVITE_DEFAULT_FROM_EMAIL',
    settings.DEFAULT_FROM_EMAIL
)
