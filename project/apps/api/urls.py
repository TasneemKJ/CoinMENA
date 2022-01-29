from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .v1.urls import urlpatterns as api_v1

urlpatterns = [
    path('v1/', include(api_v1)),
    path('auth/', obtain_auth_token, name='api_token_auth'),
]
