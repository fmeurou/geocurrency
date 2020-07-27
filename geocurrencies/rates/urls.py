from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

from .viewsets import RateViewSet, ConvertView, WatchView

app_name = 'rates'

router = routers.DefaultRouter()
router.register(r'', RateViewSet, basename='rates')

urlpatterns = [
    path('convert/', ConvertView.as_view()),
    url(r'^watch/(?P<converter_id>[0-9a-f-]{36})/$', WatchView.as_view()),
    url(r'^', include(router.urls)),
]
