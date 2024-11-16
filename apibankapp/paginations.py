# -*- coding: utf-8 -*-

from rest_framework.pagination import LimitOffsetPagination
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = "limit"
    offset_query_param = "offset"
    limit_query_description = _("Number of results to return per page.")
    offset_query_description = _("The initial index from which to return the results.")
    max_limit = 50

    def get_paginated_response(self, data):
        return JsonResponse({
                            "count": self.count,
                            "next": self.get_next_link(),
                            "previous": self.get_previous_link(),
                            "results": data})
