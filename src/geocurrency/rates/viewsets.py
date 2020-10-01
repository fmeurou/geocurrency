from datetime import datetime, date, timedelta
from django.db import models
from django.http import HttpResponseForbidden
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from geocurrency.converters.serializers import ConverterResultSerializer
from geocurrency.currencies.models import Currency
from .forms import RateForm
from .models import Rate, RateConverter
from .permissions import RateObjectPermission
from .serializers import RateSerializer, BulkSerializer, RateConversionPayloadSerializer


class RateViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    pagination_class = PageNumberPagination
    permission_classes = [RateObjectPermission]
    display_page_controls = True

    def get_queryset(self):
        if self.request.user and self.request.user.is_authenticated:
            qs = Rate.objects.filter(
                models.Q(user=self.request.user) | models.Q(user__isnull=True)
            )
            user = self.request.query_params.get('user', False)
            key = self.request.query_params.get('key', None)
            if user:
                qs = qs.filter(user=self.request.user)
            if key:
                qs = qs.filter(key=key)
        else:
            qs = Rate.objects.filter(models.Q(user__isnull=True))
        value = self.request.query_params.get('value_date', None)
        if value is not None:
            qs = qs.filter(value=value)
        lower_bound = self.request.query_params.get('lower_bound', None)
        if not value and lower_bound is not None:
            qs = qs.filter(value__gte=lower_bound)
        higher_bound = self.request.query_params.get('higher_bound', None)
        if not value and higher_bound is not None:
            qs = qs.filter(value__lte=higher_bound)
        value_date = self.request.query_params.get('value_date', None)
        if value_date:
            qs = qs.filter(value_date=value_date)
        from_date = self.request.query_params.get('from', None)
        if not value_date and from_date:
            qs = qs.filter(value_date__gte=from_date)
        to_date = self.request.query_params.get('to', None)
        if not value_date and to_date:
            qs = qs.filter(value_date__lte=to_date)
        base_currency = self.request.query_params.get('base_currency', None)
        if base_currency:
            qs = qs.filter(base_currency=base_currency)
        currency = self.request.query_params.get('currency', None)
        if currency:
            qs = qs.filter(base_currency=currency)
        return qs

    key = openapi.Parameter('key', openapi.IN_QUERY, description="Client key", type=openapi.TYPE_STRING)

    base_currency = openapi.Parameter('base_currency', openapi.IN_QUERY, description="Base currency for rate",
                                      type=openapi.TYPE_STRING)
    currency = openapi.Parameter('currency', openapi.IN_QUERY, description="Currency for rate",
                                 type=openapi.TYPE_STRING)
    from_obj = openapi.Parameter('from', openapi.IN_QUERY, description="included start of range",
                                 type=openapi.FORMAT_DATE)
    to_obj = openapi.Parameter('to', openapi.IN_QUERY, description="included end of range",
                               type=openapi.FORMAT_DATE)
    value_date = openapi.Parameter('value_date', openapi.IN_QUERY, description="date of value",
                                   type=openapi.FORMAT_DATE)
    value = openapi.Parameter('value', openapi.IN_QUERY, description="included end of range",
                              type=openapi.FORMAT_DECIMAL)
    lower_bound = openapi.Parameter('lower_bound', openapi.IN_QUERY, description="lower value bound",
                                    type=openapi.FORMAT_DECIMAL)
    higher_bound = openapi.Parameter('higher_bound', openapi.IN_QUERY, description="higher value bound",
                                     type=openapi.FORMAT_DECIMAL)
    user = openapi.Parameter('user', openapi.IN_QUERY, description="filter on current user ?",
                             type=openapi.TYPE_BOOLEAN)

    @swagger_auto_schema(manual_parameters=[user, key, base_currency, currency,
                                            value_date, from_obj, to_obj, value,
                                            lower_bound, higher_bound],
                         responses={200: RateSerializer})
    def list(self, request, *args, **kwargs):
        return super(RateViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
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
            return Response(rate_form.errors, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

    @swagger_auto_schema(method='post', request_body=BulkSerializer, responses={201: RateSerializer})
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
        return Response(serializer.data, content_type="application/json", status=status.HTTP_201_CREATED)


class ConvertView(APIView):

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
            return Response(cps.errors, status=HTTP_400_BAD_REQUEST, content_type="application/json")
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
            return Response({'id': converter.id, 'status': converter.status}, content_type="application/json")
