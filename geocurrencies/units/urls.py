from django.conf.urls import url, include
from rest_framework import routers

from .viewsets import UnitSystemViewset, UnitViewset

app_name = 'units'

router = routers.DefaultRouter()
router.register(r'', UnitSystemViewset, basename='unit_systems')
router.register(r'(?P<system_name>\w+)/units', UnitViewset, basename='units')

urlpatterns = [
    url(r'^', include(router.urls)),
]
