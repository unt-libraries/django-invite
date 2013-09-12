try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *
from django.contrib import admin

# place app url patterns here
urlpatterns = patterns(
    '',
    url(r'^$', 'invite.views.index'),
    url(r'^invite/$', 'invite.views.invite'),
    url(r'^login/$', 'invite.views.log_in_user'),
    url(r'^logout/$', 'invite.views.log_out_user'),
    url(r'^invite/send/$', 'invite.views.send'),
    url(r'^signup/$', 'invite.views.signup', name="account_signup"),
    url(r'^about/$', 'invite.views.about', name="about"),
)
