from django.urls import path
from .views import (
    WalletAddressApiView,
)

app_name = 'ticker_api_1_0'

# Browsing
urlpatterns = [
    path('addresses/<username>/<coin>/', WalletAddressApiView.as_view(), name='addresses'),
]
