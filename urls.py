from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^$', 'invite.views.index'),
    url(r'^invite/$', 'invite.views.invite', name='invite'),
    url(r'^resend/(?P<code>.*)/$', 'invite.views.resend', name='resend'),
    url(r'^revoke/(?P<code>.*)/$', 'invite.views.revoke', name='revoke'),
    url(r'^signin/$', 'invite.views.log_in_user'),
    url(r'^signout/$', 'invite.views.log_out_user'),
    url(r'^amnesia/$', 'invite.views.amnesia'),
    url(r'^reset/$', 'invite.views.reset'),
    url(r'^signup/$', 'invite.views.signup', name="account_signup"),
    url(r'^about/$', 'invite.views.about', name="about"),
)
