from django.urls import re_path

from invite import views

app_name = 'invite'
urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^invite/$', views.invite, name='invite'),
    re_path(r'^resend/(?P<code>.*)/$', views.resend, name='resend'),
    re_path(r'^revoke/(?P<code>.*)/$', views.revoke, name='revoke'),
    re_path(r'^login/$', views.log_in_user, name='login'),
    re_path(r'^logout/$', views.log_out_user, name='edit_logout'),
    re_path(r'^amnesia/$', views.amnesia, name='amnesia'),
    re_path(r'^reset/$', views.reset, name='reset'),
    re_path(r'^signup/$', views.signup, name='account_signup'),
    re_path(r'^about/$', views.about, name='about'),
    re_path(r'^check/$', views.check, name='check'),
]
