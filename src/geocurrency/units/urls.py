"""
Units module URLs
"""

from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from .views import ListFragment
from .viewsets import UnitSystemViewset, UnitViewset, ConvertView, CustomUnitViewSet, \
    ValidateViewSet, CalculationView

app_name = 'units'

router = routers.DefaultRouter()
router.register(r'', UnitSystemViewset, basename='unit_systems')
router.register(r'(?P<system_name>\w+)/units', UnitViewset, basename='units')
router.register(r'(?P<system_name>\w+)/custom', CustomUnitViewSet, basename='custom')

urlpatterns = [
    path('search/', ListFragment.as_view()),
    path('convert/', ConvertView.as_view()),
    path('<str:unit_system>/formulas/validate/', ValidateViewSet.as_view()),
    path('<str:unit_system>/formulas/calculate/', CalculationView.as_view()),
    url(r'^', include(router.urls)),
]
