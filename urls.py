from django.conf.urls import url, patterns

urlpatterns = patterns('',
    url(r'^$', 'invite.views.index', name='invite_index'),
    url(r'^invite/$', 'invite.views.invite', name='invite_invite'),
    url(r'^resend/(?P<code>.*)/$', 'invite.views.resend', name='invite_resend'),
    url(r'^revoke/(?P<code>.*)/$', 'invite.views.revoke', name='invite_revoke'),
    url(r'^login/$', 'invite.views.log_in_user', name='invite_login'),
    url(r'^logout/$', 'invite.views.log_out_user', name='invite_edit_logout'),
    url(r'^amnesia/$', 'invite.views.amnesia', name='invite_amnesia'),
    url(r'^reset/$', 'invite.views.reset', name="invite_reset"),
    url(r'^signup/$', 'invite.views.signup', name="invite_account_signup"),
    url(r'^about/$', 'invite.views.about', name="invite_about"),
)
