"""python_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from django.views import static

from web.views import home, download, about, feedback, privacy_policy, faq, tos, withoutthewatermark
from python_api.settings import STATIC_ROOT, MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    re_path(r'^$', home),
    path('home', home),
    path('about', about),
    path('feedback', feedback),
    path('downloader', download),
    path('privacy-policy', privacy_policy),
    path('faq', faq),
    path('tos', tos),
    path('withoutthewatermark', withoutthewatermark),


    re_path(r'static/(?P<path>.*)$', static.serve, {'document_root': STATIC_ROOT }, name='static'),

    #media配置——配合settings中的MEDIA_ROOT的配置，就可以在浏览器的地址栏访问media文件夹及里面的文件了
    re_path(r'media/(?P<path>.*)$', static.serve,{'document_root': MEDIA_ROOT}, name='media'),
]
