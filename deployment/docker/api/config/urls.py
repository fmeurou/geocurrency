"""GeoCurrencies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from geocurrency.countries import urls as country_urls
from geocurrency.currencies import urls as currency_urls
from geocurrency.rates import urls as rate_urls
from geocurrency.units import urls as unit_urls
from geocurrency.converters.views import WatchView
from geocurrency.core.views import index

schema_view = get_schema_view(
    openapi.Info(
        title="GeoCurrencies API",
        default_version='v1',
        description="GeoCurrencies API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email=os.environ.get('GEOCURRENCY_SERVICE_EMAIL', 'admin@peabytes.me')),
        license=openapi.License(name="BSD License"),
    ),
    url=os.environ.get('GEOCURRENCY_SERVICE_URL', 'http://127.0.0.1/'),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('currencies/', include(currency_urls)),
    path('countries/', include(country_urls)),
    path('rates/', include(rate_urls)),
    path('units/', include(unit_urls)),
    url(r'^watch/(?P<converter_id>[0-9a-f-]{36})/$', WatchView.as_view()),
    path('', index)
]