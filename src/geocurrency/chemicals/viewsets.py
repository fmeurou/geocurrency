"""
Chemicals API viewsets
"""
import chemicals
from django.core.paginator import Paginator
from django.urls import resolve, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .serializers import ChemicalMetadataListSerializer, \
    ChemicalMetadataDetailSerializer


class ChemicalViewset(ViewSet):
    """
    View for Chemicals
    """
    lookup_field = 'CASs'

    cas = openapi.Parameter(
        'CAS', openapi.IN_QUERY,
        description="CAS number",
        type=openapi.TYPE_STRING)
    cass = openapi.Parameter(
        'CASs', openapi.IN_QUERY,
        description="CAS string",
        type=openapi.TYPE_STRING)
    inchi = openapi.Parameter(
        'inchi', openapi.IN_QUERY,
        description="InChI",
        type=openapi.TYPE_STRING)
    common_name = openapi.Parameter(
        'common_name', openapi.IN_QUERY,
        description="Common name",
        type=openapi.TYPE_STRING)
    formula = openapi.Parameter(
        'formula', openapi.IN_QUERY,
        description="Formula",
        type=openapi.TYPE_STRING)
    iupac_name = openapi.Parameter(
        'iupac_name', openapi.IN_QUERY,
        description="CAS string",
        type=openapi.TYPE_STRING)
    pubchemid = openapi.Parameter(
        'pubchemid', openapi.IN_QUERY,
        description="Pubchem ID",
        type=openapi.TYPE_NUMBER)
    search = openapi.Parameter(
        'search', openapi.IN_HEADER,
        description="search",
        type=openapi.TYPE_STRING)
    language_header = openapi.Parameter(
        'Accept-Language', openapi.IN_HEADER,
        description="language",
        type=openapi.TYPE_STRING)
    language = openapi.Parameter(
        'language',
        openapi.IN_QUERY,
        description="language",
        type=openapi.TYPE_STRING)
    ordering = openapi.Parameter(
        'ordering', openapi.IN_QUERY,
        description="Sort on name, alpha_2, alpha_3, numeric. "
                    "Prefix with - for descending sort",
        type=openapi.TYPE_STRING)
    page = openapi.Parameter(
        'page', openapi.IN_QUERY,
        description="A page number within the paginated result set.",
        type=openapi.TYPE_INTEGER)
    page_size = openapi.Parameter(
        'page_size', openapi.IN_QUERY,
        description="Number of results to return per page.",
        type=openapi.TYPE_INTEGER)

    def _filter_chemicals(self, request, chems):
        filters = ['CAS', 'CASs', 'InChI', 'common_name',
                   'formula', 'pubchemid']
        chem_list = []
        if request.GET.get('search'):
            term = request.GET.get('search')
            for filter in filter:
                chem_list += [c for c in chems if term in getattr(c, filter)]
            chem_list = list(set(chem_list))
        else:
            chem_list = chems
        for filter in filters:
            value = request.GET.get(filter)
            if value:
                if isinstance(getattr(chemicals.identifiers.ChemicalMetadata,
                                      filter), str):
                    chem_list = [c for c in chem_list
                                 if value in getattr(c, filter)]
                elif isinstance(getattr(chemicals.identifiers.ChemicalMetadata,
                                        filter), int):
                    chem_list = [c for c in chem_list
                                 if int(value) == getattr(c, filter)]
                elif isinstance(getattr(chemicals.identifiers.ChemicalMetadata,
                                        filter), float):
                    chem_list = [c for c in chem_list
                                 if float(value) == getattr(c, filter)]
                else:
                    chem_list = [c for c in chem_list
                                 if value == getattr(c, filter)]
        return chem_list

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_cookie)
    @swagger_auto_schema(
        manual_parameters=[
            cas,
            cass,
            inchi,
            common_name,
            formula,
            iupac_name,
            pubchemid,
            search,
            language,
            language_header,
            ordering,
            page,
            page_size])
    def list(self, request):
        """
        List chemicals. this view is not paginated
        """
        db = chemicals.identifiers.ChemicalMetadataDB()
        db.autoload_main_db()
        ordering = request.GET.get('ordering', 'common_name')
        if ordering not \
                in ChemicalMetadataListSerializer.CHEMICAL_METADATA_FIELDS:
            ordering = 'common_name'
        chem_list = self._filter_chemicals(request, db.pubchem_index.values())
        chem_list = sorted(chem_list,
                           key=lambda x: getattr(x, ordering))
        try:
            page = int(request.GET.get('page'))
        except ValueError:
            page = 1
        try:
            page_size = int(request.GET.get('page_size', 100))
        except ValueError:
            page_size = 100

        p = Paginator(chem_list, page_size)
        p_list = p.page(page)
        serializer = ChemicalMetadataListSerializer(
            p_list,
            many=True,
            context={'request': request})
        result = {
            'count': p.count,
            'next': f"{reverse('chemicals:chemicals-list')}"
                    f"?page={page + 1}&page_size={page_size}",
            'previous': f"{reverse('chemicals:chemicals-list')}"
                    f"?page={page - 1}&page_size={page_size}",
            'results': serializer.data
        }
        return Response(result, content_type='application/json')

    def retrieve(self, request, CASs):
        """
        Show details of a chemical component
        """
        db = chemicals.identifiers.ChemicalMetadataDB()
        db.autoload_main_db()
        try:
            chem = db.search_CAS(CASs)
            serializer = ChemicalMetadataDetailSerializer(
                chem,
                context={'request': request})
            return Response(serializer.data)
        except ValueError as e:
            print(e)
            return Response("Invalid CAS value",
                            status=status.HTTP_404_NOT_FOUND)
