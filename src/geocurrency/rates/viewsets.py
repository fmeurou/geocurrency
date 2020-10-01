from datetime import datetime, date, timedelta
from django.db import models
from django.http import HttpResponseForbidden
from django_filters import rest_framework as filters
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

from .filters import RateFilter
from .forms import RateForm
from .models import Rate, RateConverter
from .permissions import RateObjectPermission
from .serializers import RateSerializer, BulkSerializer, RateConversionPayloadSerializer


class RateViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RateFilter
    pagination_class = PageNumberPagination
    permission_classes = [RateObjectPermission]
    display_page_controls = True

    def get_queryset(self):
        qs = super(RateViewSet, self).get_queryset()
        if self.request.user and self.request.user.is_authenticated:
            qs = qs.filter(
                models.Q(user=self.request.user) | models.Q(user__isnull=True)
            )
        else:
            qs = qs.filter(models.Q(user__isnull=True))
        return qs

    currency_latest_values = openapi.Parameter('currency_latest_values', openapi.IN_QUERY,
                                               description="Currency to filter on, limits results to latest values",
                                               type=openapi.TYPE_STRING)
    base_currency_latest_values = openapi.Parameter(
        'base_currency_latest_values', openapi.IN_QUERY,
        description="Base currency to filter on, limits results to latest values",
        type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[currency_latest_values, base_currency_latest_values],
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
