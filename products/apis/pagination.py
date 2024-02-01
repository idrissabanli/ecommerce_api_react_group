from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import logging

log = logging.getLogger(__name__)


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_paginated_response_with_result_keyword(self, data, result_keyword):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            (result_keyword, data)
        ]))


class CustomPageNumberPaginationWithPageNumber(CustomPageNumberPagination):

    def get_next_link(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return page_number

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        return page_number

    def get_paginated_response_with_result_keyword(self, data, result_keyword):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            (result_keyword, data)
        ]))
