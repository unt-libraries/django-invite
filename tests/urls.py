from django.urls import include, path

urlpatterns = [
    path('', include('invite.urls', namespace='invite')),
]
