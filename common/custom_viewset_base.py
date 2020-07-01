# -*- coding: utf-8 -*-
# @Time    : 2020-06-29 16:34
# @Author  : chenshiyang
# @Email   : chenshiyang@blued.com
# @File    : custom_viewset_base.py
# @Software: PyCharm

from rest_framework import status
from rest_framework import viewsets
from common.jsonresponse import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class CustomViewBase(viewsets.ModelViewSet):

    # filter_class = ServerFilter
    queryset = None
    serializer_class = None
    # permission_classes = ()
    filter_fields = ()
    # search_fields = ()

    filter_backends = (OrderingFilter, DjangoFilterBackend)

    def create(self, request, *args, **kwargs):
        self.request_class = request
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(data=serializer.data, msg="success", statusCode='000000',
                            status=status.HTTP_201_CREATED, headers=headers)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data, statusCode='000000', msg="success", status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(data=serializer.data, statusCode='000000', msg="success", status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        self.request_class = request
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        self.update_log(instance)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return JsonResponse(data=serializer.data, msg="success", statusCode='000000', status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        # instance = self.get_object()
        # self.perform_destroy(instance)

        instance = self.get_object()
        instance.status = 1
        instance.save()
        return JsonResponse(data=[], statusCode='000000', msg="delete resource success", status=status.HTTP_200_OK)
