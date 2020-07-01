import re
from urllib.parse import urlparse

import requests
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from common.custom_viewset_base import CustomViewBase
from common.utils import format_duration


class DouyinModelViewSet(CustomViewBase):
    """
        list:
        返回对应配置信息列表

        retrieve:
        返回配置信息详情

        create:
        创建配置

        update:
        修改配置

        destroy:
        删除配置
    """

    serializer_class = None
    queryset = None

    # 过滤
    filter_fields = ('id',)

    # 排序
    ordering_fields = ('id',)

    permission_classes = (AllowAny,)



    headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': 'sid_guard=2e624045d2da7f502b37ecf72974d311%7C1591170698%7C5184000%7CSun%2C+02-Aug-2020+07%3A51%3A38+GMT; uid_tt=0033579d9229eec4a4d09871dfc11271; sid_tt=2e624045d2da7f502b37ecf72974d311; sessionid=2e624045d2da7f502b37ecf72974d311',
            'pragma': 'no-cache',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
        }

    domain = ['www.douyin.com',
                       'v.douyin.com',
                       'www.snssdk.com',
                       'www.amemv.com',
                       'www.iesdouyin.com',
                       'aweme.snssdk.com']


    @action(methods=['post', 'get'], detail=True)
    def parse(self, request, pk):
        url = request.data.get('url', None) or request.POST.get('url', None)

        assert url != None

        share_url = self.get_share_url(url)
        share_url_parse = urlparse(share_url)

        if share_url_parse.netloc not in self.domain:
            raise Exception("无效的链接")

        dytk = None
        vid = re.findall(r'\/share\/video\/(\d*)', share_url_parse.path)[0]
        match = re.search(r'\/share\/video\/(\d*)', share_url_parse.path)
        if match:
            vid = match.group(1)

        response = requests.get(
            share_url,
            headers=self.headers,
            allow_redirects=False)

        match = re.search('dytk: "(.*?)"', response.text)

        if match:
            dytk = match.group(1)

        if vid:
            data = self.get_data(vid, dytk)
            # return Response({"statusCode": "000000", "messages": "success", "data":data}, status=status.HTTP_200_OK)
            ret = Response({"statusCode": "000000", "messages": "success", "data":data}, status=status.HTTP_200_OK)
            ret['Access-Control-Allow-Origin'] = "*"
            return ret
        else:
            raise Exception("解析失败")

    def get_share_url(self, url):
        response = requests.get(url,
                                headers=self.headers,
                                allow_redirects=False)
        if 'location' in response.headers.keys():
            return response.headers['location']
        else:
            raise Exception("解析失败")

    def get_data(self, vid, dytk):
        url = f"https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={vid}&dytk={dytk}"
        response = requests.get(url, headers=self.headers, )
        result = response.json()
        if not response.status_code == 200:
            raise Exception("解析失败")

        item = result.get("item_list")[0]
        author = item.get("author").get("nickname")
        mp4 = item.get("video").get("play_addr").get("url_list")[0]
        cover = item.get("video").get("cover").get("url_list")[0]
        mp4 = mp4.replace("playwm", "play")
        res = requests.get(mp4, headers=self.headers, allow_redirects=True)
        mp4 = res.url
        desc = item.get("desc")
        mp3 = item.get("music").get("play_url").get("url_list")[0]

        data = dict()
        data['mp3'] = mp3
        data['mp4'] = mp4
        data['cover'] = cover
        data['nickname'] = author
        data['desc'] = desc
        data['duration'] = format_duration(item.get("duration"))
        return data

    @action(methods=['POST', 'GET'], detail=True)
    def get_mp4(self, request, pk):
        url = request.data.get('url', None)
        print('url--------', url)
        assert url != None

        url = "https://aweme.snssdk.com/aweme/v1/play/?video_id=v0200fe70000br155v26tgq06h08e0lg&ratio=720p&line=0"

        payload = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text.encode('utf8'))
        ret = Response({"statusCode": "000000", "messages": "success", "data": response.text.encode('utf8')}, status=status.HTTP_200_OK)
        ret['Access-Control-Allow-Origin'] = "*"
        return ret