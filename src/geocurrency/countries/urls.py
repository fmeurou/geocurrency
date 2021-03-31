"""
Country URLs
"""

from django.conf.urls import url, include
from django.urls import path

from rest_framework import routers

from .views import FlagView, TurboCountryListView
from .viewsets import CountryViewset

app_name = 'countries'

router = routers.DefaultRouter()
router.register(r'', CountryViewset, basename='countries')

urlpatterns = [
    path('search/', TurboCountryListView.as_view()),
    url(r'^', include(router.urls)),
    url(r'^(?P<pk>[^/.]+)/flag/$', FlagView.as_view())
]
