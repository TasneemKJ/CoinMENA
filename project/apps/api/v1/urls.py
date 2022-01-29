from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import RateViews

urlpatterns = [
    path('quotes', RateViews.as_view(), name='api_quotes'),
]
