"""
Chemicals URLs
"""

from django.conf.urls import url, include
from rest_framework import routers

from .viewsets import ChemicalViewset

app_name = 'chemicals'

router = routers.DefaultRouter()
router.register(r'', ChemicalViewset, basename='chemicals')

urlpatterns = [
    url(r'^', include(router.urls)),
]
