from django.conf.urls import url, include
from rest_framework import routers

from .viewsets import RateViewSet

app_name = 'rates'

router = routers.DefaultRouter()
router.register(r'', RateViewSet, basename='rates')

urlpatterns = [
    url(r'^', include(router.urls)),
]
