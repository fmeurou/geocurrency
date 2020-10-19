from rest_framework import pagination
from django.conf import settings
from .settings import MAX_PAGE_SIZE


class PageNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = getattr(settings, 'GEOCURRENCY_MAX_PAGE_SIZE', MAX_PAGE_SIZE)

