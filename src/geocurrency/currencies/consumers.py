"""
Country consumer
"""
import datetime

from channels.consumer import SyncConsumer
from django.template import loader

from .models import Currency


class PublicCurrencyConsumer(SyncConsumer):
    """
    Public websocket consumer for Currencies
    """

    def websocket_connect(self, event):
        """
        Handle connection request
        """
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        """
        Handle request for a currency
        """
        currencies = Currency.search(term=event['text'])
        template = loader.get_template(template_name='stream.html')
        context = {
            'dom_id': 'currencies_stream',
            'action': 'replace',
            'model_template': 'currencies/partial/list.html',
            'currencies': currencies,
            'timestamp': datetime.datetime.now().timestamp()
        }
        self.send({
            "type": "websocket.send",
            "text": template.render(context=context),
        })
