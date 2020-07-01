# -*- coding: utf-8 -*-
# @Time    : 2020-06-29 16:51
# @Author  : chenshiyang
# @Email   : chenshiyang@blued.com
# @File    : urls.py
# @Software: PyCharm

from api.views import *

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
# router.register(r'project', ProjectModelViewSet, basename='project')
router.register(r'dytk', DouyinModelViewSet, basename='dytk')

urlpatterns = router.urls
