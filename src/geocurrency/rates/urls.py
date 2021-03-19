"""
Rates module URLs
"""

from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

from .viewsets import RateViewSet, ConvertView

app_name = 'rates'

router = routers.DefaultRouter()
router.register(r'', RateViewSet, basename='rates')

urlpatterns = [
    path('convert/', ConvertView.as_view()),
    url(r'^', include(router.urls)),
]
