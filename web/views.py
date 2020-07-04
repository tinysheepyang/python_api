from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from common.utils import format_duration, load_media
from common.DouYin import DY
from web.forms import FeedbakForm


def home(request):
    """首页"""

    return render(request, 'home.html')


def about(request):
    """关于"""

    return render(request, 'about.html')

def download(request):
    """下载"""

    url = request.POST.get('url', None)

    assert url != None

    dy = DY()
    data = dy.parse(url)

    mp4_path, mp4_content_length = load_media(data['mp4'], 'mp4')
    mp3_path, mp3_content_length = load_media(data['mp3'], 'mp3')

    realpath = ''.join(['https://www.chenshiyang.com', mp4_path])

    print('realpath---------------------', realpath)

    if len(data['desc'].split('#')) > 2:
        topic = data['desc'].split('#')[2].rstrip('#')

    return render(request, 'download.html', locals())

def feedback(request):
    """反馈"""

    if request.method == 'POST':
        uf = FeedbakForm(request.POST)

        if uf.is_valid():
            uf.save()
            return redirect('/home')

    return render(request, 'feedback.html', locals())


def privacy_policy(request):
    """隐私政策"""

    return render(request, 'privacy-policy.html', locals())


def faq(request):
    """常见问题"""

    return render(request, 'faq.html', locals())


def tos(request):
    """使用条款"""

    return render(request, 'tos.html', locals())


def withoutthewatermark(request):
    """如何下载无水印视频"""

    return render(request, 'withoutthewatermark.html', locals())