# mysite/asgi.py
import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import OriginValidator
from django.conf.urls import url
from django.core.asgi import get_asgi_application
from geocurrency.countries.consumers import PublicCountryConsumer
from geocurrency.currencies.consumers import PublicCurrencyConsumer
from geocurrency.rates.consumers import PublicRateConsumer
from geocurrency.units.consumers import PublicUnitConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
    # WebSocket chat handler
    "websocket": OriginValidator(
        URLRouter([
            url(r"^countries/$", PublicCountryConsumer.as_asgi()),
            url(r"^currencies/$", PublicCurrencyConsumer.as_asgi()),
            url(r"^rates/$", PublicRateConsumer.as_asgi()),
            url(r"^units/$", PublicUnitConsumer.as_asgi()),
        ]),
        ['https://api.geocurrency.me', 'https://dev.geocurrency.me', 'http://127.0.0.1:8000']
    ),
})
