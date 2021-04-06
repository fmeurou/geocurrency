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
from django.conf.urls import url, include
from django.urls import path
from .converters.views import WatchView
from .countries import urls as country_urls
from .currencies import urls as currency_urls
from .rates import urls as rate_urls
from .units import urls as unit_urls

urlpatterns = [
    path('currencies/', include(currency_urls)),
    path('countries/', include(country_urls)),
    path('rates/', include(rate_urls)),
    path('units/', include(unit_urls)),
    url(r'^watch/(?P<converter_id>[0-9a-f-]{36})/$', WatchView.as_view()),
]
