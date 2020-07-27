from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.viewsets import ViewSet

from .models import Unit, UnitSystem
from .serializers import UnitSerializer, UnitSystemListSerializer, UnitSystemDetailSerializer


class UnitSystemViewset(ViewSet):
    """
    View for currency
    """

    def list(self, request):
        us = [UnitSystem(system=s) for s in UnitSystem.available_systems()]
        serializer = UnitSystemListSerializer(us, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk):
        try:
            us = UnitSystem(system=pk)
            serializer = UnitSystemDetailSerializer(us, context={'request': request})
            return Response(serializer.data, content_type="application/json")
        except ValueError:
            return Response("Unknown unit system", status=HTTP_404_NOT_FOUND)


class UnitViewset(ViewSet):
    """
    View for currency
    """
    def list(self, request):
        units = [UnitSystem(system=s) for s in UnitSystem.available_systems()]
        serializer = UnitSystemListSerializer(units, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk):
        try:
            us = UnitSystem(system=pk)
            serializer = UnitSystemDetailSerializer(us, context={'request': request})
            return Response(serializer.data, content_type="application/json")
        except ValueError:
            return Response("Unknown unit system", status=HTTP_404_NOT_FOUND)

