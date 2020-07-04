# -*- coding: utf-8 -*-
# @Time    : 2020-06-29 17:26
# @Author  : chenshiyang
# @Email   : chenshiyang@blued.com
# @File    : utils.py
# @Software: PyCharm
import os
import time

import requests


def format_duration(duration):
    """
    格式化时长
    :param duration 毫秒
    """

    total_seconds = int(duration / 1000)
    minute = total_seconds // 60
    seconds = total_seconds % 60
    return f'{minute:02}:{seconds:02}'

SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
    1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']}


def approximate_size(size, a_kilobyte_is_1024_bytes=True):

    '''Convert a file size to human-readable form.

    Keyword arguments:
    size -- file size in bytes
    a_kilobyte_is_1024_bytes -- if True (default), use multiples of 1024
                                if False, use multiples of 1000

    Returns: string

    '''

    if size < 0:
        raise ValueError('number must be non-negative')

    multiple = 1024 if a_kilobyte_is_1024_bytes else 1000
    for suffix in SUFFIXES[multiple]:
        size /= multiple
        if size < multiple:
            return '{0:.1f} {1}'.format(size, suffix)

    raise ValueError('number too large')


def do_load_media(url, path):
    """
    对媒体下载
    :param url:         多媒体地址
    :param path:        文件保存路径
    :return:            None
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"}
        pre_content_length = 0

        # 循环接收视频数据
        while True:
            # 若文件已经存在，则断点续传，设置接收来需接收数据的位置
            if os.path.exists(path):
                headers['Range'] = 'bytes=%d-' % os.path.getsize(path)
            res = requests.get(url, stream=True, headers=headers)

            content_length = int(res.headers['content-length'])
            # 若当前报文长度小于前次报文长度，或者已接收文件等于当前报文长度，则可以认为视频接收完成
            if content_length < pre_content_length or (
                    os.path.exists(path) and os.path.getsize(path) == content_length):
                break
            pre_content_length = content_length

            # 写入收到的视频数据
            with open(path, 'ab') as file:
                file.write(res.content)
                file.flush()
                print('receive data，file size : %d   total size:%d' % (os.path.getsize(path), content_length))
                return approximate_size(content_length, a_kilobyte_is_1024_bytes=False)

    except Exception as e:
        print('视频下载异常:{}'.format(e))


def load_media(url, path):

    basepath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    # 生成13位时间戳
    suffixes = str(int(round(time.time() * 1000)))
    path = ''.join(['/media/', path, '/', '.'.join([suffixes, path])])
    targetpath = ''.join([basepath, path])
    content_length = do_load_media(url, targetpath)
    return path, content_length


def main(url, suffixes, path):
    load_media(url, suffixes, path)


if __name__ == "__main__":
    # url = 'https://aweme.snssdk.com/aweme/v1/play/?video_id=v0200fe70000br155v26tgq06h08e0lg&ratio=720p&line=0'
    # suffixes = 'test'
    # main(url, suffixes, 'mp4',)

    print(approximate_size(3726257, a_kilobyte_is_1024_bytes=False))
