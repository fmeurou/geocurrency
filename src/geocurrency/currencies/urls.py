"""
URLs for currencies module
"""

from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

from .viewsets import CurrencyViewset
from .views import TurboCurrencyListView

app_name = 'currencies'

router = routers.DefaultRouter()
router.register(r'', CurrencyViewset, basename='currencies')

urlpatterns = [
    path('search/', TurboCurrencyListView.as_view()),
    url(r'^', include(router.urls)),
]
