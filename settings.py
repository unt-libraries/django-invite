from django.conf import settings
from django.core.urlresolvers import reverse_lazy

INVITE_LOGOUT_REDIRECT_URL = getattr(settings, 'INVITE_LOGOUT_REDIRECT_URL', reverse_lazy('index'))

