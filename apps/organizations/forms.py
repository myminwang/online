#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "问道编程"
__date__ = "2018-06-06 18:40"

import re

from django import forms
from operation.models import UserAsk


class UserAskForm(forms.Form):
    """用户咨询验证"""

    class Meta:
        """继承UserAsk类"""
        model = UserAsk
        fileds = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """自定义手机号验证"""
        mobile = self.cleaned_data['mobile']  # 取其中的一个值，其中cleaned_data是Form的一个属性，字典，取自所有form验证通过的数据
        p = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
        if p.match(mobile):
            # 这里还可以返回外键
            return mobile
        raise forms.ValidationError('手机号码格式不对', code='mobile_inval')