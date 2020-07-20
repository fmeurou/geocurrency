from django.conf.urls import url, include
from rest_framework import routers

from .viewsets import CountryViewset
from .views import FlagView

app_name = 'countries'

router = routers.DefaultRouter()
router.register(r'', CountryViewset, basename='countries')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^(?P<pk>[^/.]+)/flag/$', FlagView.as_view())
]
