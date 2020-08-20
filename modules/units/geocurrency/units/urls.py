from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

from .viewsets import UnitSystemViewset, UnitViewset, ConvertView

app_name = 'units'

router = routers.DefaultRouter()
router.register(r'', UnitSystemViewset, basename='unit_systems')
router.register(r'(?P<system_name>\w+)/units', UnitViewset, basename='units')

urlpatterns = [
    path('convert/', ConvertView.as_view()),
    url(r'^', include(router.urls)),
]
