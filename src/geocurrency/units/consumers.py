"""
Units consumer
"""
import datetime

from channels.consumer import SyncConsumer
from django.template import loader

from .models import UnitSystem


class PublicUnitConsumer(SyncConsumer):
    """
    Public consumer for Unit
    """

    def websocket_connect(self, event):
        """
        Websocket connect handler
        :param event: received connect event
        """
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        """
        Websocket receive handler
        :param event: event with text containing unit name
        """
        unit_system = UnitSystem()
        dest_units = [unit_system.unit(str(u)) for u in unit_system.ureg.get_compatible_units(
            input_units=event.get('text', 'meter'))]
        template = loader.get_template(template_name='units/partial/dest_units.html')
        context = {
            'dom_id': 'dest_units_list',
            'action': 'replace',
            'dest_units': dest_units,
            'timestamp': datetime.datetime.now().timestamp()
        }
        self.send({
            "type": "websocket.send",
            "text": template.render(context=context),
        })
