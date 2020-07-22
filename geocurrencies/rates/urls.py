from django.conf.urls import url, include
from rest_framework import routers

from .viewsets import RateViewset

app_name = 'rates'

router = routers.DefaultRouter()
router.register(r'', RateViewset, basename='rates')

urlpatterns = [
    url(r'^', include(router.urls)),
]
