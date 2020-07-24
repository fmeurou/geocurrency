from django.conf.urls import url
from django.urls import path
from rest_framework import routers

from .viewsets import ConvertView, WatchView

app_name = 'convert'

urlpatterns = [
    path('', ConvertView.as_view()),
    url(r'^(?P<pk>[^/.]+)/$', WatchView.as_view())
]
