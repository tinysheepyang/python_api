# -*- coding: utf-8 -*-
# @Time    : 2020-07-03 16:16
# @Author  : chenshiyang
# @Email   : chenshiyang@blued.com
# @File    : forms.py
# @Software: PyCharm

from django import forms
from web.models import feedback


class FeedbakForm(forms.ModelForm):

    class Meta:
        model = feedback
        fields = '__all__'
