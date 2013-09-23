try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *
from django.contrib import admin

# place app url patterns here
urlpatterns = patterns(
    '',
    url(r'^$', 'invite.views.index'),
    url(r'^invite/$', 'invite.views.invite', name='invite'),
    url(r'^resend/(?P<code>.*)/$', 'invite.views.resend', name='resend'),
    url(r'^login/$', 'invite.views.log_in_user'),
    url(r'^logout/$', 'invite.views.log_out_user'),
    url(r'^signup/$', 'invite.views.signup', name="account_signup"),
    url(r'^about/$', 'invite.views.about', name="about"),
)
