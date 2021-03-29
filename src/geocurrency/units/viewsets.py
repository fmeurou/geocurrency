"""
Units module APIs viewsets
"""

import json
import logging

from django.db import models
from django.http import HttpResponseForbidden, HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django_filters import rest_framework as filters
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from geocurrency.converters.models import ConverterLoadError
from geocurrency.converters.serializers import ConverterResultSerializer, \
    CalculationResultSerializer
from geocurrency.core.helpers import validate_language
from geocurrency.core.pagination import PageNumberPagination
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet

from . import DIMENSIONS
from .exceptions import UnitConverterInitError, UnitSystemNotFound, UnitNotFound, \
    DimensionNotFound, ExpressionCalculatorInitError, UnitValueError
from .filters import CustomUnitFilter
from .forms import CustomUnitForm
from .models import UnitSystem, UnitConverter, Dimension, CustomUnit, ExpressionCalculator
from .permissions import CustomUnitObjectPermission
from .renderers import UnitsRenderer
from .serializers import UnitSerializer, UnitSystemSerializer, \
    UnitConversionPayloadSerializer, DimensionSerializer, \
    DimensionWithUnitsSerializer, CustomUnitSerializer, ExpressionSerializer, \
    CalculationPayloadSerializer


class UnitSystemViewset(ViewSet):
    """
    View for currency
    """
    lookup_field = 'system_name'

    language_header = openapi.Parameter('Accept-Language', openapi.IN_HEADER,
                                        description="language",
                                        type=openapi.TYPE_STRING)
    language = openapi.Parameter('language', openapi.IN_QUERY,
                                 description="language",
                                 type=openapi.TYPE_STRING)

    unit_systems_response = openapi.Response('List of unit systems', UnitSystemSerializer)
    unit_system_response = openapi.Response('Dimensions and units in a system',
                                            UnitSystemSerializer)

    ordering = openapi.Parameter('ordering', openapi.IN_QUERY,
                                 description="Sort on name "
                                             "Prefix with - for descending sort",
                                 type=openapi.TYPE_STRING)

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_cookie)
    @swagger_auto_schema(manual_parameters=[language, language_header, ordering],
                         responses={200: unit_systems_response})
    def list(self, request):
        """
        List UnitSystems
        """
        ordering = request.GET.get('ordering', 'system_name')
        descending = False
        if ordering and ordering[0] == '-':
            ordering = ordering[1:]
            descending = True
        if ordering not in ['system_name']:
            ordering = 'system_name'
        language = validate_language(request.GET.get('language', request.LANGUAGE_CODE))
        us = UnitSystem(fmt_locale=language)
        us = [{'system_name': s} for s in sorted(us.available_systems(), reverse=descending)]
        return Response(us, content_type="application/json")

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_cookie)
    @swagger_auto_schema(manual_parameters=[language, language_header],
                         responses={200: unit_system_response})
    def retrieve(self, request, system_name):
        """
        Retrieve UnitSystem
        """
        language = validate_language(request.GET.get('language', request.LANGUAGE_CODE))
        try:
            us = UnitSystem(system_name=system_name, fmt_locale=language)
            serializer = UnitSystemSerializer(us, context={'request': request})
            return Response(serializer.data, content_type="application/json")
        except UnitSystemNotFound as e:
            return Response("Unknown unit system: " + str(e), status=HTTP_404_NOT_FOUND)

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_cookie)
    @swagger_auto_schema(manual_parameters=[language, language_header, ordering],
                         responses={200: DimensionSerializer})
    @action(methods=['GET'], detail=True, name='dimensions', url_path='dimensions')
    def dimensions(self, request, system_name):
        """
        List Dimensions of a UnitSystem
        """
        language = validate_language(request.GET.get('language', request.LANGUAGE_CODE))
        ordering = request.GET.get('ordering', 'name')
        try:
            us = UnitSystem(system_name=system_name, fmt_locale=language)
            serializer = DimensionSerializer(us.available_dimensions(ordering=ordering),
                                             many=True,
                                             context={'request': request})
            return Response(serializer.data, content_type="application/json")
        except UnitSystemNotFound as e:
            return Response("Unknown unit system: " + str(e), status=HTTP_404_NOT_FOUND)


class UnitViewset(ViewSet):
    """
    View for currency
    """
    lookup_field = 'unit_name'
    language_header = openapi.Parameter('Accept-Language', openapi.IN_HEADER,
                                        description="language",
                                        type=openapi.TYPE_STRING)
    language = openapi.Parameter('language', openapi.IN_QUERY, description="language",
                                 type=openapi.TYPE_STRING)
    dimension = openapi.Parameter('dimension', openapi.IN_QUERY, description="Unit dimension",
                                  type=openapi.TYPE_STRING)
    key = openapi.Parameter('key', openapi.IN_QUERY,
                            description="key",
                            type=openapi.TYPE_STRING)
    units_response = openapi.Response('List of units in a system', UnitSerializer)
    unit_response = openapi.Response('Detail of a unit', UnitSerializer)
    dimension_response = openapi.Response('List of units per dimension',
                                          DimensionWithUnitsSerializer)
    ordering = openapi.Parameter('ordering', openapi.IN_QUERY,
                                 description="Sort on fields name or code. "
                                             "Prefix with - for descending sort",
                                 type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[dimension, key,
                                            ordering,
                                            language, language_header],
                         responses={200: units_response})
    def list(self, request: HttpRequest, system_name: str):
        """
        List Units, ordered, filtered by key or dimension, translated in language
        """
        language = validate_language(request.GET.get('language', request.LANGUAGE_CODE))
        ordering = request.GET.get('ordering', 'name')
        descending = False
        if ordering and ordering[0] == '-':
            ordering = ordering[1:]
            descending = True
        if ordering not in ['code', 'name']:
            ordering = 'name'
        try:
            key = request.GET.get('key', None)
            user = request.user if hasattr(request,
                                           'user') and request.user.is_authenticated else None
            us = UnitSystem(system_name=system_name, fmt_locale=language, user=user, key=key)
            units = []
            if dimension_param := request.GET.get(key='dimension'):
                try:
                    dimension = Dimension(unit_system=us, code=dimension_param)
                    units = dimension.units(user=user, key=key)
                except DimensionNotFound:
                    return Response('Invalid dimension filter', status=status.HTTP_400_BAD_REQUEST)
            else:
                available_units = us.available_unit_names()
                if available_units:
                    units = [us.unit(unit_name=unit_name) for unit_name in available_units]
            units = sorted(units, key=lambda x: getattr(x, ordering), reverse=descending)
            serializer = UnitSerializer(units, many=True, context={'request': request})
            return Response(serializer.data)
        except UnitSystemNotFound:
            return Response('Invalid Unit System', status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(manual_parameters=[key, language, language_header],
                         responses={200: dimension_response})
    @action(['GET'], detail=False, name='units per dimension', url_path='per_dimension')
    def list_per_dimension(self, request: HttpRequest, system_name: str):
        """
        List Units grouped by dimension, filter on key, translated
        """
        language = validate_language(request.GET.get('language', request.LANGUAGE_CODE))
        try:
            key = request.GET.get('key', None)
            user = request.user if hasattr(request,
                                           'user') and request.user.is_authenticated else None
            us = UnitSystem(system_name=system_name, fmt_locale=language, user=user, key=key)
            dimensions = [Dimension(unit_system=us, code=code) for code in DIMENSIONS.keys()]
            serializer = DimensionWithUnitsSerializer(dimensions, many=True,
                                                      context={'request': request})
            return Response(serializer.data)
        except UnitSystemNotFound as e:
            logging.warning(str(e))
            return Response('Invalid Unit System', status=status.HTTP_404_NOT_FOUND)

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_cookie)
    @swagger_auto_schema(manual_parameters=[key, language, language_header],
                         responses={200: unit_response})
    def retrieve(self, request: HttpRequest, system_name: str, unit_name: str):
        """
        Get unit information for unit in unit system
        """
        language = validate_language(request.GET.get('language', request.LANGUAGE_CODE))
        try:
            key = request.GET.get('key', None)
            user = request.user if hasattr(request,
                                           'user') and request.user.is_authenticated else None
            us = UnitSystem(system_name=system_name, fmt_locale=language, user=user, key=key)
            unit = us.unit(unit_name=unit_name)
            serializer = UnitSerializer(unit, context={'request': request})
            return Response(serializer.data, content_type="application/json")
        except (UnitSystemNotFound, UnitNotFound):
            return Response("Unknown unit", status=HTTP_404_NOT_FOUND)

    @swagger_auto_schema(manual_parameters=[language, language_header, ordering],
                         responses={200: units_response})
    @action(methods=['GET'], detail=True, url_path='compatible', url_name='compatible_units')
    def compatible_units(self, request: HttpRequest, system_name: str, unit_name: str):
        """
        List compatible Units
        """
        language = validate_language(request.GET.get('language', request.LANGUAGE_CODE))
        ordering = request.GET.get('ordering', 'name')
        descending = False
        if ordering and ordering[0] == '-':
            ordering = ordering[1:]
            descending = True
        if ordering not in ['code', 'name']:
            ordering = 'name'
        try:
            key = request.GET.get('key', None)
            user = request.user if hasattr(request,
                                           'user') and request.user.is_authenticated else None
            us = UnitSystem(system_name=system_name, fmt_locale=language, user=user, key=key)
            unit = us.unit(unit_name=unit_name)
            compatible_units = sorted([us.unit(unit_name=cunit) for cunit in
                                       map(str, unit.unit.compatible_units())],
                                      key=lambda x: getattr(x, ordering),
                                      reverse=descending)
            serializer = UnitSerializer(compatible_units, many=True, context={'request': request})
            return Response(serializer.data, content_type="application/json")
        except (UnitSystemNotFound, UnitNotFound):
            return Response("Unknown unit", status=HTTP_404_NOT_FOUND)


class ConvertView(APIView):
    """
    Convert Units API
    """

    @swagger_auto_schema(request_body=UnitConversionPayloadSerializer,
                         responses={200: ConverterResultSerializer})
    @action(['POST'], detail=False, url_path='', url_name="convert")
    def post(self, request, *args, **kwargs):
        """
        Converts a list of amounts with currency and date to a reference currency
        :param request: HTTP request
        """
        cps = UnitConversionPayloadSerializer(data=request.data)
        if not cps.is_valid():
            return Response(cps.errors, status=HTTP_400_BAD_REQUEST,
                            content_type="application/json")
        cp = cps.create(cps.validated_data)
        user = None
        if request.user and request.user.is_authenticated:
            user = request.user
        key = request.POST.get('key', None)
        try:
            converter = UnitConverter.load(user=user, key=key, id=cp.batch_id)
        except ConverterLoadError:
            converter = UnitConverter(
                id=cp.batch_id,
                base_system=cp.base_system,
                base_unit=cp.base_unit,
                user=user,
                key=key
            )
        except UnitConverterInitError:
            return Response("Error initializing converter", status=status.HTTP_400_BAD_REQUEST)
        if cp.data:
            if errors := converter.add_data(data=cp.data):
                return Response(errors, status=HTTP_400_BAD_REQUEST)
        if cp.eob or not cp.batch_id:
            result = converter.convert()
            serializer = ConverterResultSerializer(result)
            return Response(serializer.data, content_type="application/json")
        else:
            return Response({'id': converter.id, 'status': converter.status},
                            content_type="application/json")


class CustomUnitViewSet(ModelViewSet):
    """
    Custom Units API
    """
    queryset = CustomUnit.objects.all()
    serializer_class = CustomUnitSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CustomUnitFilter
    pagination_class = PageNumberPagination
    permission_classes = [CustomUnitObjectPermission, permissions.IsAuthenticated]
    display_page_controls = True
    lookup_url_param = 'system_name'

    user = openapi.Parameter('user',
                             openapi.IN_QUERY,
                             description="Filter on user rates",
                             type=openapi.TYPE_BOOLEAN)
    key = openapi.Parameter('key',
                            openapi.IN_QUERY,
                            description="Filter on user defined category",
                            type=openapi.TYPE_STRING)
    unit_system = openapi.Parameter('unit_system',
                                    openapi.IN_QUERY,
                                    description="Filter on unit system",
                                    type=openapi.TYPE_STRING)
    code = openapi.Parameter('code',
                             openapi.IN_QUERY,
                             description="Filter on unit code",
                             type=openapi.TYPE_STRING)
    name = openapi.Parameter('name',
                             openapi.IN_QUERY,
                             description="Filter on unit name",
                             type=openapi.TYPE_STRING)
    relation = openapi.Parameter('relation',
                                 openapi.IN_QUERY,
                                 description="Filter on relation to base units",
                                 type=openapi.TYPE_STRING)
    symbol = openapi.Parameter('symbol',
                               openapi.IN_QUERY,
                               description="Filter on unit symbol",
                               type=openapi.TYPE_STRING)
    alias = openapi.Parameter('alias',
                              openapi.IN_QUERY,
                              description="Filter on unit alias",
                              type=openapi.TYPE_STRING)
    ordering = openapi.Parameter('ordering',
                                 openapi.IN_QUERY,
                                 description="Sort on code, name, relation, symbol, alias. "
                                             "Prefix with - for descending sort",
                                 type=openapi.TYPE_STRING)

    def get_queryset(self):
        """
        Filter units based on authenticated user
        """
        qs = super(CustomUnitViewSet, self).get_queryset()
        system_name = self.kwargs.get(self.lookup_url_param, 'SI')
        if self.request.user and self.request.user.is_authenticated:
            qs = qs.filter(
                models.Q(user=self.request.user) | models.Q(user__isnull=True)
            )
            if self.request.GET.get('key'):
                qs = qs.filter(key=self.request.GET.get('key'))
        else:
            qs = qs.filter(models.Q(user__isnull=True))
        qs = qs.filter(unit_system__iexact=system_name.lower())
        return qs

    @swagger_auto_schema(manual_parameters=[
        user, key, unit_system, code, name, relation, symbol, alias, ordering],
        responses={200: CustomUnitSerializer})
    def list(self, request, *args, **kwargs):
        """
        List rates
        """
        return super().list(request, *args, **kwargs)

    def create(self, request: HttpRequest, system_name: str, *args, **kwargs):
        """
        Create CustomUnit
        """
        cu_form = CustomUnitForm(request.data)
        if cu_form.is_valid():
            cu = cu_form.save(commit=False)
            try:
                us = UnitSystem(system_name=system_name, user=request.user, key=cu.key)
            except UnitSystemNotFound:
                return Response("Invalid unit system", status=status.HTTP_400_BAD_REQUEST)
            if request.user and request.user.is_authenticated:
                if CustomUnit.objects.filter(code=cu.code, user=request.user, key=cu.key).exists():
                    return Response("Custom unit already exists", status=status.HTTP_409_CONFLICT)
                cu.user = request.user
                cu.unit_system = system_name
                try:
                    cu.save()
                except (UnitValueError, ValueError) as e:
                    return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
                serializer = CustomUnitSerializer(cu)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return HttpResponseForbidden()
        else:
            return Response(cu_form.errors, status=status.HTTP_400_BAD_REQUEST,
                            content_type="application/json")


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
            us = UnitSystem(unit_system, user=request.user, key=request.data.get('key', None))
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
    renderer_classes = [UnitsRenderer]

    @swagger_auto_schema(request_body=CalculationPayloadSerializer,
                         responses={200: CalculationResultSerializer})
    @action(['POST'], detail=False, url_path='', url_name="convert")
    def post(self, request, *args, **kwargs):
        """
        Converts a list of amounts with currency and date to a reference currency
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
            calculator = ExpressionCalculator.load(user=user, key=key, id=cp.batch_id)
        except ConverterLoadError:
            calculator = ExpressionCalculator(
                id=cp.batch_id,
                unit_system=cp.unit_system,
                user=user,
                key=key
            )
        except ExpressionCalculatorInitError:
            return Response("Error initializing calculator", status=status.HTTP_400_BAD_REQUEST)
        if cp.data:
            if errors := calculator.add_data(data=cp.data):
                return Response(errors, status=HTTP_400_BAD_REQUEST)
        if cp.eob or not cp.batch_id:
            result = calculator.convert()
            serializer = CalculationResultSerializer(result)
            return Response(serializer.data, content_type="application/json")
        else:
            return Response({'id': calculator.id, 'status': calculator.status},
                            content_type="application/json")
