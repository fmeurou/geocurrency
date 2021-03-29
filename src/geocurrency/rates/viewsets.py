"""
Rates modules API viewsets
"""

from django.db import models
from django.db.models.functions import Extract
from django.http import HttpResponseForbidden
from django_filters import rest_framework as filters
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from geocurrency.converters.serializers import ConverterResultSerializer
from geocurrency.core.pagination import PageNumberPagination
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .filters import RateFilter
from .forms import RateForm
from .models import Rate, RateConverter
from .permissions import RateObjectPermission
from .serializers import RateSerializer, BulkSerializer, RateConversionPayloadSerializer, \
    RateStatSerializer


class RateViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    Rate API
    """
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RateFilter
    pagination_class = PageNumberPagination
    permission_classes = [RateObjectPermission]
    display_page_controls = True

    def get_queryset(self):
        """
        Filter on connected user
        """
        qs = super(RateViewSet, self).get_queryset()
        if self.request.user and self.request.user.is_authenticated:
            qs = qs.filter(
                models.Q(user=self.request.user) | models.Q(user__isnull=True)
            )
        else:
            qs = qs.filter(models.Q(user__isnull=True))
        return qs

    user = openapi.Parameter(
        'user',
        openapi.IN_QUERY,
        description="Filter on user rates",
        type=openapi.TYPE_BOOLEAN)
    key = openapi.Parameter(
        'key',
        openapi.IN_QUERY,
        description="Filter on user defined category",
        type=openapi.TYPE_STRING)
    key_or_null = openapi.Parameter(
        'key_or_null',
        openapi.IN_QUERY,
        description="Show rates with defined category or no category",
        type=openapi.TYPE_STRING)
    key_isnull = openapi.Parameter(
        'key_isnull',
        openapi.IN_QUERY,
        description="ONly show results with no category",
        type=openapi.TYPE_STRING)
    value_date = openapi.Parameter(
        'value_date',
        openapi.IN_QUERY,
        description="Filter on date of the rate",
        type=openapi.TYPE_STRING)
    from_obj = openapi.Parameter(
        'from_obj',
        openapi.IN_QUERY,
        description="Filter rates with value date after date",
        type=openapi.TYPE_STRING)
    to_obj = openapi.Parameter(
        'to_obj',
        openapi.IN_QUERY,
        description="Filter rates with value date before date",
        type=openapi.TYPE_STRING)
    value = openapi.Parameter(
        'value',
        openapi.IN_QUERY,
        description="Filter rates with a specific value",
        type=openapi.TYPE_NUMBER)
    lower_bound = openapi.Parameter(
        'lower_bound',
        openapi.IN_QUERY,
        description="Filter rates with a value higher than value",
        type=openapi.TYPE_NUMBER)
    higher_bound = openapi.Parameter(
        'higher_bound',
        openapi.IN_QUERY,
        description="Filter rates with a value lower than value",
        type=openapi.TYPE_NUMBER)
    currency = openapi.Parameter(
        'currency',
        openapi.IN_QUERY,
        description="Filter by currency",
        type=openapi.TYPE_STRING)
    base_currency = openapi.Parameter(
        'base_currency',
        openapi.IN_QUERY,
        description="Filter by base currency",
        type=openapi.TYPE_STRING)

    currency_latest_values = openapi.Parameter(
        'currency_latest_values',
        openapi.IN_QUERY,
        description="Currency to filter on, limits results to latest values",
        type=openapi.TYPE_STRING)
    base_currency_latest_values = openapi.Parameter(
        'base_currency_latest_values',
        openapi.IN_QUERY,
        description="Base currency to filter on, limits results to latest values",
        type=openapi.TYPE_STRING)

    period = openapi.Parameter(
        'period',
        openapi.IN_QUERY,
        description="period to aggregate on: month, week, year, defaults to month",
        type=openapi.TYPE_STRING)

    ordering = openapi.Parameter('ordering',
                                 openapi.IN_QUERY,
                                 description="Sort on currency, base_currency, value_date, value. "
                                             "Prefix with - for descending sort",
                                 type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[
        user, key, key_or_null, key_isnull, value_date, from_obj, to_obj, value,
        lower_bound, higher_bound, currency, base_currency,
        currency_latest_values, base_currency_latest_values, ordering],
        responses={200: RateSerializer})
    def list(self, request, *args, **kwargs):
        """
        List rates
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            user, key, key_or_null, key_isnull, value_date, from_obj, to_obj, value,
            lower_bound, higher_bound, currency, base_currency,
            currency_latest_values, base_currency_latest_values, period],
        responses={200: RateStatSerializer})
    @action(['GET'], detail=False, url_path='stats', url_name='stats')
    def stats(self, request, *args, **kwargs):
        """
        stats on rates
        """
        period = request.GET.get('period', 'month')
        if period not in ['week', 'month', 'year']:
            return Response("Invalid period", status=status.HTTP_400_BAD_REQUEST)
        rate_filter = RateFilter(request.GET, queryset=self.queryset, request=request)
        qs = rate_filter.qs.values('currency', 'base_currency')
        if period == 'month':
            qs = qs.annotate(month=Extract('value_date', 'month'))
        if period == 'week':
            qs = qs.annotate(week=Extract('value_date', 'week'))
        qs = qs.annotate(
            year=Extract('value_date', 'year'),
            avg=models.Avg('value'),
            max=models.Max('value'),
            min=models.Min('value'),
            std_dev=models.StdDev('value')
        ).order_by('-year', '-' + period)
        results = [
            {
                'currency': result['currency'],
                'base_currency': result['base_currency'],
                'period': f"{result['year']}-{str(result[period]).zfill(2)}"
                if period != 'year'
                else result['year'],
                'avg': result['avg'],
                'max': result['max'],
                'min': result['min'],
                'std_dev': result['std_dev'],
            }
            for result in qs
        ]
        data = {
            'key': request.GET.get('key'),
            'period': period,
            'from_date': request.GET.get('from_date', ''),
            'to_date': request.GET.get('to_date', ''),
            'results': results
        }
        serializer = RateStatSerializer(data)
        return Response(serializer.data, content_type="application/json")

    def create(self, request, *args, **kwargs):
        """
        Create a new rate
        """
        rate_form = RateForm(request.data)
        if rate_form.is_valid():
            rate = rate_form.save(commit=False)
            if request.user and request.user.is_authenticated:
                rate.user = request.user
                rate.save()
                serializer = RateSerializer(rate)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return HttpResponseForbidden()
        else:
            return Response(rate_form.errors, status=status.HTTP_400_BAD_REQUEST,
                            content_type="application/json")

    @swagger_auto_schema(method='post', request_body=BulkSerializer,
                         responses={201: RateSerializer})
    @action(['POST'], detail=False, url_path='bulk', url_name="bulk_create")
    def create_bulk(self, request):
        """
        Create rates for user on a range of dates
        """
        if not request.user or not request.user.is_authenticated:
            return HttpResponseForbidden()
        bs = BulkSerializer(data=request.data)
        if not bs.is_valid():
            return Response(bs.errors, status=status.HTTP_400_BAD_REQUEST)
        bulk_rate = bs.create(validated_data=bs.validated_data)
        rates = bulk_rate.to_rates(user=request.user)
        serializer = RateSerializer(rates, many=True)
        return Response(serializer.data, content_type="application/json",
                        status=status.HTTP_201_CREATED)


class ConvertView(APIView):
    """
    Conversion API
    """

    @swagger_auto_schema(request_body=RateConversionPayloadSerializer,
                         responses={200: ConverterResultSerializer})
    @action(['POST'], detail=False, url_path='', url_name="convert")
    def post(self, request, *args, **kwargs):
        """
        Converts a list of amounts with currency and date to a reference currency
        :param request: HTTP request
        """
        cps = RateConversionPayloadSerializer(data=request.data)
        if not cps.is_valid():
            return Response(cps.errors, status=HTTP_400_BAD_REQUEST,
                            content_type="application/json")
        cp = cps.create(cps.validated_data)
        try:
            converter = RateConverter.load(cp.batch_id)
        except KeyError:
            converter = RateConverter(
                id=cp.batch_id,
                user=request.user,
                key=cp.key,
                base_currency=cp.target
            )
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
