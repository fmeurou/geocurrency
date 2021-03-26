"""
Renderer for Units
"""

import json
from rest_framework.renderers import JSONRenderer
from rest_framework.settings import api_settings
from rest_framework.utils.encoders import JSONEncoder

from .models import Operand


class UnitsEncoder(JSONEncoder):
    """
    Encoder for Custom Unit
    """

    def default(self, obj):
        if isinstance(obj, Operand):
            return json.dumps({'name': obj.name, 'value': obj.value, 'unit': obj.unit})
        else:
            return super().default(obj)


class UnitsRenderer(JSONRenderer):
    """
    Renderer which serializes to JSON with UnitsEncoder
    """
    media_type = 'application/json'
    format = 'json'
    encoder_class = UnitsEncoder
    ensure_ascii = not api_settings.UNICODE_JSON
    compact = api_settings.COMPACT_JSON
    strict = api_settings.STRICT_JSON

    # We don't set a charset because JSON is a binary encoding,
    # that can be encoded as utf-8, utf-16 or utf-32.
    # See: https://www.ietf.org/rfc/rfc4627.txt
    # Also: http://lucumr.pocoo.org/2013/7/19/application-mimetypes-and-encodings/
    charset = None
