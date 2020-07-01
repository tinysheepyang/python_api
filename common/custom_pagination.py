# -*- coding: utf-8 -*-
# @Time    : 2020-06-29 16:40
# @Author  : chenshiyang
# @Email   : chenshiyang@blued.com
# @File    : custom_pagination.py  自定义分页
# @Software: PyCharm

from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from collections import OrderedDict
from rest_framework.response import Response


class LargeResultsSetPagination(LimitOffsetPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def get_paginated_response(self, data):
        statusCode = '000000'
        msg = 'success'
        if not data:
            statusCode = '100000'
            msg = "Data Not Found"

        return Response(OrderedDict([
            ('statusCode', statusCode),
            ('msg', msg),
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('datalist', data),
        ]))