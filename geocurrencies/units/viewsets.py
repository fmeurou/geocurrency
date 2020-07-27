from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.viewsets import ViewSet

from .models import Unit, UnitSystem
from .serializers import UnitSerializer, UnitSystemListSerializer, UnitSystemDetailSerializer


class UnitSystemViewset(ViewSet):
    """
    View for currency
    """
    lookup_field = 'system_name'

    def list(self, request):
        us = UnitSystem()
        us = [UnitSystem(system_name=s) for s in us.available_systems()]
        serializer = UnitSystemListSerializer(us, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, system_name):
        try:
            us = UnitSystem(system_name=system_name)
            serializer = UnitSystemDetailSerializer(us, context={'request': request})
            return Response(serializer.data, content_type="application/json")
        except (ValueError, KeyError):
            return Response("Unknown unit system", status=HTTP_404_NOT_FOUND)


class UnitViewset(ViewSet):
    """
    View for currency
    """
    lookup_field='unit_name'

    def list(self, request, system_name):
        try:
            us = UnitSystem(system_name=system_name)
            units = [us.unit(unit_name=unit_name) for unit_name in us.available_unit_names()]
            serializer = UnitSerializer(units, many=True, context={'request': request})
            return Response(serializer.data)
        except KeyError:
            return Response('Invalid Unit System', status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, system_name, unit_name):
        """
        Get unit information for unit in unit system
        """
        try:
            us = UnitSystem(system_name=system_name)
            unit = us.unit(unit_name=unit_name)
            serializer = UnitSerializer(unit, context={'request': request})
            return Response(serializer.data, content_type="application/json")
        except (ValueError, KeyError):
            return Response("Unknown unit", status=HTTP_404_NOT_FOUND)

