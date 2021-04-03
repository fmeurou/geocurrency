"""
Rates consumer
"""
import datetime

from channels.consumer import SyncConsumer
from django.template import loader

from .models import Rate
from geocurrency.currencies.models import Currency


class PublicRateConsumer(SyncConsumer):
    """
    Public consumer for rates
    Returns a list of rates as a HTML fragment
    """

    def websocket_connect(self, event):
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        """
        Handle request for rates
        :param event: dict containing search parameters
        """
        from_currency = event.get('from_currency', 'USD')
        to_currency = event.get('to_currency', 'EUR')
        from_date = event.get('from_date', '')
        to_date = event.get('to_date', '')
        if from_date:
            from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
        else:
            from_date = datetime.date.today() - datetime.timedelta(7)
        if to_date:
            to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d')
        else:
            to_date = datetime.date.today()
        template = loader.get_template(template_name='stream.html')
        context = {
            'currencies': Currency.all_currencies(),
            'from_date': from_date,
            'to_date': to_date,
            'from_currency': from_currency,
            'to_currency': to_currency,
            'rates': Rate.objects.filter(
                currency=from_currency,
                base_currency=to_currency,
                value_date__gte=from_date,
                value_date__lte=to_date
            ),
            'timestamp': datetime.datetime.now().timestamp()
        }
        self.send({
            "type": "websocket.send",
            "text": template.render(context=context),
        })
