#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "问道编程"
__date__ = "2018-06-06 18:40"

import re

from django import forms
from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    """用户咨询验证,注意这里继承的是ModelForm"""

    class Meta:
        """继承UserAsk类"""
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """自定义手机号验证"""
        mobile = self.cleaned_data['mobile']
        p = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
        if p.match(mobile):
            return mobile
        raise forms.ValidationError('手机号码格式不对', code='mobile_inval')
