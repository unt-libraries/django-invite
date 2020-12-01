from django.urls import path

from invite import views

app_name = 'invite'
urlpatterns = [
    path('$', views.index, name='index'),
    path('invite/$', views.invite, name='invite'),
    path('resend/(?P<code>.*)/$', views.resend, name='resend'),
    path('revoke/(?P<code>.*)/$', views.revoke, name='revoke'),
    path('login/$', views.log_in_user, name='login'),
    path('logout/$', views.log_out_user, name='edit_logout'),
    path('amnesia/$', views.amnesia, name='amnesia'),
    path('reset/$', views.reset, name='reset'),
    path('signup/$', views.signup, name='account_signup'),
    path('about/$', views.about, name='about'),
    path('check/$', views.check, name='check'),
]
