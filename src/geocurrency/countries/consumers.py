"""
Country consumer
"""
import datetime

from channels.consumer import SyncConsumer
from django.template import loader

from .models import Country


class PublicCountryConsumer(SyncConsumer):
    """
    Public websocket consumer for Countries.
    Returns a turbo stream
    """

    def websocket_connect(self, event):
        """
        Handle connection
        """
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        """
        Handle request for fragment
        """
        countries = Country.search(term=event['text'])
        template = loader.get_template(template_name='stream.html')
        context = {
            'dom_id': 'countries_stream',
            'action': 'replace',
            'model_template': 'countries/partial/list.html',
            'countries': countries,
            'timestamp': datetime.datetime.now().timestamp()
        }
        self.send({
            "type": "websocket.send",
            "text": template.render(context=context),
        })
