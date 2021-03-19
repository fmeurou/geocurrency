"""
URLs for currencies module
"""

from django.conf.urls import url, include
from rest_framework import routers

from .viewsets import CurrencyViewset

app_name = 'currencies'

router = routers.DefaultRouter()
router.register(r'', CurrencyViewset, basename='currencies')

urlpatterns = [
    url(r'^', include(router.urls)),
]
