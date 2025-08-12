import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


logger = logging.getLogger(__name__)


class StandardPagination(PageNumberPagination):
    """Standard pagination class for all APIs"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'success': True,
            'code': status.HTTP_200_OK,
            'message': 'Data retrieved successfully',
            'data': data,
            'pagination': {
                'count': self.page.paginator.count,
                'page': self.page.number,
                'page_size': self.page.paginator.per_page,
                'total_pages': self.page.paginator.num_pages,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'has_next': self.page.has_next(),
                'has_previous': self.page.has_previous(),
            }
        })