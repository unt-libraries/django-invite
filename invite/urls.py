from django.conf.urls import url

from invite import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^invite/$', views.invite, name='invite'),
    url(r'^resend/(?P<code>.*)/$', views.resend, name='resend'),
    url(r'^revoke/(?P<code>.*)/$', views.revoke, name='revoke'),
    url(r'^login/$', views.log_in_user, name='login'),
    url(r'^logout/$', views.log_out_user, name='edit_logout'),
    url(r'^amnesia/$', views.amnesia, name='amnesia'),
    url(r'^reset/$', views.reset, name='reset'),
    url(r'^signup/$', views.signup, name='account_signup'),
    url(r'^about/$', views.about, name='about'),
]
