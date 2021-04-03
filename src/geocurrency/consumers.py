"""
Geocurrency consumer
"""

from channels.consumer import SyncConsumer


class PublicConsumer(SyncConsumer):
    """
    Public consumer for generic websocket connection.
    """

    def websocket_connect(self, event):
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        self.send({
            "type": "websocket.send",
            "text": "Hello websocket client!",
        })
