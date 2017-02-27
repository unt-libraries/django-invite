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


INVITE_DEFAULT_FROM_EMAIL = getattr(
    settings,
    'INVITE_DEFAULT_FROM_EMAIL',
    settings.DEFAULT_FROM_EMAIL
)


def get_service_name(request=None):
    """
    INVITE_SERVICE_NAME

    Constants are set when the application bootstraps.
    With an empty database, an exception will be thrown and will
    prevent the database from being synced, because the django_sites table does
    not yet exist. To workaround that the INVITE_SERVICE_NAME settings is
    wrapped in this callable.
    """
    return getattr(
        settings,
        'INVITE_SERVICE_NAME',
        Site.objects.get_current(request=request).name)
