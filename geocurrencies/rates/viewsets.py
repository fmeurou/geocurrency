from django.conf import settings
from django.db import models
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination

from .models import Rate
from .serializers import RateSerializer
from .permissions import RateObjectPermission


class RateViewset(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    pagination_class = PageNumberPagination
    permission_classes = [RateObjectPermission]
    display_page_controls = True

    def get_queryset(self):
        return Rate.objects.filter(
            models.Q(user=self.request.user)|models.Q(user__isnull=True)
        )
