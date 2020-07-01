# -*- coding: utf-8 -*-
# @Time    : 2020-06-29 17:26
# @Author  : chenshiyang
# @Email   : chenshiyang@blued.com
# @File    : utils.py
# @Software: PyCharm


def format_duration(duration):
    """
    格式化时长
    :param duration 毫秒
    """

    total_seconds = int(duration / 1000)
    minute = total_seconds // 60
    seconds = total_seconds % 60
    return f'{minute:02}:{seconds:02}'