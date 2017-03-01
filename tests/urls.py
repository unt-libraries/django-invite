from django.conf.urls import include, url

urlpatterns = [
    url(r'^', include('invite.urls', namespace='invite')),
]
