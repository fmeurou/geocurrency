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
from geocurrency.converters.serializers import ConverterResultSerializer
from geocurrency.core.helpers import validate_language
from geocurrency.core.pagination import PageNumberPagination
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet

from . import DIMENSIONS
from .exceptions import UnitConverterInitError, UnitSystemNotFound, UnitNotFound, DimensionNotFound
from .filters import CustomUnitFilter
from .forms import CustomUnitForm
from .models import UnitSystem, UnitConverter, Dimension, CustomUnit
from .permissions import CustomUnitObjectPermission
from .serializers import UnitSerializer, UnitSystemSerializer, \
    UnitConversionPayloadSerializer, DimensionSerializer, \
    DimensionWithUnitsSerializer, CustomUnitSerializer


class UnitSystemViewset(ViewSet):
    """
    View for currency
    """
    lookup_field = 'system_name'

    language_header = openapi.Parameter('Accept-Language', openapi.IN_HEADER, description="language",
                                        type=openapi.TYPE_STRING)
    language = openapi.Parameter('language', openapi.IN_QUERY,
                                 description="language",
                                 type=openapi.TYPE_STRING)

    unit_systems_response = openapi.Response('List of unit systems', UnitSystemSerializer)
    unit_system_response = openapi.Response('Dimensions and units in a system', UnitSystemSerializer)

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_cookie)
    @swagger_auto_schema(manual_parameters=[language, language_header], responses={200: unit_systems_response})
    def list(self, request):
        language = validate_language(request.GET.get('language', request.LANGUAGE_CODE))
        us = UnitSystem(fmt_locale=language)
        us = [{'system_name': s} for s in us.available_systems()]
        return Response(us, content_type="application/json")

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_cookie)
    @swagger_auto_schema(manual_parameters=[language, language_header], responses={200: unit_system_response})
    def retrieve(self, request, system_name):
        language = validate_language(request.GET.get('language', request.LANGUAGE_CODE))
        try:
            us = UnitSystem(system_name=system_name, fmt_locale=language)
            serializer = UnitSystemSerializer(us, context={'request': request})
            return Response(serializer.data, content_type="application/json")
        except UnitSystemNotFound as e:
            return Response("Unknown unit system: " + str(e), status=HTTP_404_NOT_FOUND)

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_cookie)
    @swagger_auto_schema(manual_parameters=[language, language_header], responses={200: DimensionSerializer})
    @action(methods=['GET'], detail=True, name='dimensions', url_path='dimensions')
    def dimensions(self, request, system_name):
        language = validate_language(request.GET.get('language', request.LANGUAGE_CODE))
        try:
            us = UnitSystem(system_name=system_name, fmt_locale=language)
            serializer = DimensionSerializer(us.available_dimensions(), many=True, context={'request': request})
            return Response(serializer.data, content_type="application/json")
        except UnitSystemNotFound as e:
            return Response("Unknown unit system: " + str(e), status=HTTP_404_NOT_FOUND)


class UnitViewset(ViewSet):
    """
    View for currency
    """
    lookup_field = 'unit_name'
    language_header = openapi.Parameter('Accept-Language', openapi.IN_HEADER, description="language",
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
    dimension_response = openapi.Response('List of units per dimension', DimensionWithUnitsSerializer)

    @swagger_auto_schema(manual_parameters=[dimension, key, language, language_header], responses={200: units_response})
    def list(self, request: HttpRequest, system_name: str):
        language = validate_language(request.GET.get('language', request.LANGUAGE_CODE))
        try:
            key = request.GET.get('key', None)
            user = request.user if hasattr(request, 'user') and request.user.is_authenticated else None
            us = UnitSystem(system_name=system_name, fmt_locale=language, user=user, key=key)
            units = []
            if dimension_param := request.GET.get('dimension'):
                try:
                    dimension = Dimension(unit_system=us, code=dimension_param)
                    units = dimension.units(user=user, key=key)
                except DimensionNotFound:
                    return Response('Invalid dimension filter', status=status.HTTP_400_BAD_REQUEST)
            else:
                available_units = us.available_unit_names()
                if available_units:
                    units = [us.unit(unit_name=unit_name) for unit_name in available_units]
            serializer = UnitSerializer(units, many=True, context={'request': request})
            return Response(serializer.data)
        except UnitSystemNotFound:
            return Response('Invalid Unit System', status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(manual_parameters=[key, language, language_header], responses={200: dimension_response})
    @action(['GET'], detail=False, name='units per dimension', url_path='per_dimension')
    def list_per_dimension(self, request: HttpRequest, system_name: str):
        language = validate_language(request.GET.get('language', request.LANGUAGE_CODE))
        try:
            key = request.GET.get('key', None)
            user = request.user if hasattr(request, 'user') and request.user.is_authenticated else None
            us = UnitSystem(system_name=system_name, fmt_locale=language, user=user, key=key)
            dimensions = [Dimension(unit_system=us, code=code) for code in DIMENSIONS.keys()]
            serializer = DimensionWithUnitsSerializer(dimensions, many=True, context={'request': request})
            return Response(serializer.data)
        except UnitSystemNotFound as e:
            logging.warning(str(e))
            return Response('Invalid Unit System', status=status.HTTP_404_NOT_FOUND)

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_cookie)
    @swagger_auto_schema(manual_parameters=[key, language, language_header], responses={200: unit_response})
    def retrieve(self, request: HttpRequest, system_name: str, unit_name: str):
        """
        Get unit information for unit in unit system
        """
        language = validate_language(request.GET.get('language', request.LANGUAGE_CODE))
        try:
            key = request.GET.get('key', None)
            user = request.user if hasattr(request, 'user') and request.user.is_authenticated else None
            us = UnitSystem(system_name=system_name, fmt_locale=language, user=user, key=key)
            unit = us.unit(unit_name=unit_name)
            serializer = UnitSerializer(unit, context={'request': request})
            return Response(serializer.data, content_type="application/json")
        except (UnitSystemNotFound, UnitNotFound):
            return Response("Unknown unit", status=HTTP_404_NOT_FOUND)

    @swagger_auto_schema(manual_parameters=[language, language_header], responses={200: units_response})
    @action(methods=['GET'], detail=True, url_path='compatible', url_name='compatible_units')
    def compatible_units(self, request: HttpRequest, system_name: str, unit_name: str):
        language = validate_language(request.GET.get('language', request.LANGUAGE_CODE))
        try:
            key = request.GET.get('key', None)
            user = request.user if hasattr(request, 'user') and request.user.is_authenticated else None
            us = UnitSystem(system_name=system_name, fmt_locale=language, user=user, key=key)
            unit = us.unit(unit_name=unit_name)
            compatible_units = [us.unit(unit_name=cunit) for cunit in map(str, unit.unit.compatible_units())]
            serializer = UnitSerializer(compatible_units, many=True, context={'request': request})
            return Response(serializer.data, content_type="application/json")
        except (UnitSystemNotFound, UnitNotFound):
            return Response("Unknown unit", status=HTTP_404_NOT_FOUND)


class ConvertView(APIView):

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
            return Response(cps.errors, status=HTTP_400_BAD_REQUEST, content_type="application/json")
        cp = cps.create(cps.validated_data)
        try:
            converter = UnitConverter.load(cp.batch_id)
        except ConverterLoadError:
            converter = UnitConverter(
                id=cp.batch_id,
                base_system=cp.base_system,
                base_unit=cp.base_unit
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
            return Response({'id': converter.id, 'status': converter.status}, content_type="application/json")


class CustomUnitViewSet(ModelViewSet):
    queryset = CustomUnit.objects.all()
    serializer_class = CustomUnitSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CustomUnitFilter
    pagination_class = PageNumberPagination
    permission_classes = [CustomUnitObjectPermission, permissions.IsAuthenticated]
    display_page_controls = True

    def get_queryset(self):
        qs = super(CustomUnitViewSet, self).get_queryset()
        if self.request.user and self.request.user.is_authenticated:
            qs = qs.filter(
                models.Q(user=self.request.user) | models.Q(user__isnull=True)
            )
            if self.request.GET.get('key'):
                qs = qs.filter(key=self.request.GET.get('key'))
        else:
            qs = qs.filter(models.Q(user__isnull=True))
        return qs

    def create(self, request: HttpRequest, system_name: str, *args, **kwargs):
        cu_form = CustomUnitForm(request.data)
        if cu_form.is_valid():
            cu = cu_form.save(commit=False)
            try:
                us = UnitSystem(system_name=system_name, user=request.user, key=cu.key)
            except UnitSystemNotFound:
                return Response("Invalid unit system", status=status.HTTP_400_BAD_REQUEST)
            if request.user and request.user.is_authenticated:
                cu.user = request.user
                cu.unit_system = system_name
                cu.save()
                serializer = CustomUnitSerializer(cu)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return HttpResponseForbidden()
        else:
            return Response(cu_form.errors, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")
