from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class AddressFilterBackend(DjangoFilterBackend):

    def get_filterset_kwargs(self, request, queryset, view):
        return {
            'data': request.data,
            'queryset': queryset,
            'request': request,
        }

class AddressSearchFilter(SearchFilter):

    def get_search_terms(self, request):
        """
        Search terms are set by a ?search=... query parameter,
        and may be comma and/or whitespace delimited.
        """
        params = request.data.get(self.search_param, '')
        params = params.replace('\x00', '')  # strip null characters
        params = params.replace(',', ' ')
        return params.split()
