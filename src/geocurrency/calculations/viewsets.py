"""
Calculations module APIs viewsets
"""

import json

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from geocurrency.converters.models import ConverterLoadError
from geocurrency.units.models import UnitSystem
from .exceptions import ExpressionCalculatorInitError
from .models import ExpressionCalculator
from .renderers import OperandUnitsRenderer
from .serializers import ExpressionSerializer, \
    CalculationPayloadSerializer, CalculationResultSerializer


class ValidateViewSet(APIView):
    """
    POST API View to validate formulas
    """

    @swagger_auto_schema(request_body=ExpressionSerializer)
    @action(['POST'], detail=False, url_path='', url_name="validate")
    def post(self, request, unit_system, *args, **kwargs):
        """
        Validate a formula with parameters
        :param request: HTTP request
        :param unit_system: Unit system to use for validation
        """
        if request.user and request.user.is_authenticated:
            us = UnitSystem(
                unit_system,
                user=request.user,
                key=request.data.get('key', None))
        else:
            us = UnitSystem(unit_system)
        exp = ExpressionSerializer(data=request.data)
        if exp.is_valid(unit_system=us, dimensions_only=True):
            return Response("Valid expression")
        else:
            return Response(json.dumps(exp.errors),
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                            content_type="application/json")


class CalculationView(APIView):
    """
    Calculate a batch of formulas
    """
    renderer_classes = [OperandUnitsRenderer]

    @swagger_auto_schema(request_body=CalculationPayloadSerializer,
                         responses={200: CalculationResultSerializer})
    @action(['POST'], detail=False, url_path='', url_name="convert")
    def post(self, request, *args, **kwargs):
        """
        Converts a list of amounts with currency
        and date to a reference currency
        :param request: HTTP request
        """
        cps = CalculationPayloadSerializer(data=request.data)
        if not cps.is_valid():
            return Response(cps.errors, status=HTTP_400_BAD_REQUEST,
                            content_type="application/json")
        cp = cps.create(cps.validated_data)
        user = None
        if request.user and request.user.is_authenticated:
            user = request.user
        key = request.POST.get('key', None)
        try:
            calculator = ExpressionCalculator.load(
                user=user,
                key=key,
                id=cp.batch_id)
        except ConverterLoadError:
            calculator = ExpressionCalculator(
                id=cp.batch_id,
                unit_system=cp.unit_system,
                user=user,
                key=key
            )
        except ExpressionCalculatorInitError:
            return Response("Error initializing calculator",
                            status=status.HTTP_400_BAD_REQUEST)
        if cp.data:
            errors = calculator.add_data(data=cp.data)
            if errors:
                return Response(errors, status=HTTP_400_BAD_REQUEST)
        if cp.eob or not cp.batch_id:
            result = calculator.convert()
            serializer = CalculationResultSerializer(result)
            return Response(serializer.data, content_type="application/json")
        else:
            return Response({'id': calculator.id, 'status': calculator.status},
                            content_type="application/json")
