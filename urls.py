from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^$', 'invite.views.index', name='index'),
    url(r'^invite/$', 'invite.views.invite', name='invite'),
    url(r'^resend/(?P<code>.*)/$', 'invite.views.resend', name='resend'),
    url(r'^revoke/(?P<code>.*)/$', 'invite.views.revoke', name='revoke'),
    url(r'^login/$', 'invite.views.log_in_user', name='login'),
    url(r'^logout/$', 'invite.views.log_out_user', name='edit_logout'),
    url(r'^amnesia/$', 'invite.views.amnesia', name='amnesia'),
    url(r'^reset/$', 'invite.views.reset', name="reset"),
    url(r'^signup/$', 'invite.views.signup', name="account_signup"),
    url(r'^about/$', 'invite.views.about', name="about"),
)
