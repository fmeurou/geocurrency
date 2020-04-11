from django.conf.urls import url, include
from rest_framework import routers

from .viewsets import CountryViewset

app_name = 'countries'

router = routers.DefaultRouter()
router.register(r'', CountryViewset)

urlpatterns = [
    url(r'^', include(router.urls)),
]
