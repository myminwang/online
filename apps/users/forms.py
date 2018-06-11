#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "问道编程"
__date__ = "5/30/18 12:31"

import re
from django import forms
from captcha.fields import CaptchaField  # 验证码验证模块

from .models import UserProfile


class RegisterForm(forms.Form):
    """注册信息验证"""
    # 通过验证，传回对象，验证失败，传回错误信息
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6, max_length=20)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class LoginForm(forms.Form):
    """登录信息验证"""
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6, max_length=20)


class ForgetpwdForm(forms.Form):
    """忘记密码信息验证"""
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class PwdmodifyForm(forms.Form):
    """密码重置信息验证"""
    password1 = forms.CharField(required=True, min_length=6, max_length=20)
    password2 = forms.CharField(required=True, min_length=6, max_length=20)


class UpImageForm(forms.ModelForm):
    """个人中心修改头像验证"""

    class Meta:
        model = UserProfile
        fields = ['image']


class UpUserInfoForm(forms.ModelForm):
    """个人中心的个人资料的修改"""

    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile']

    # def clean_mobile(self):
    #     """自定义手机号验证"""
    #     mobile = self.cleaned_data['mobile']  # cleaned_data是Form的一个属性，字典，取自所有form验证通过的数据
    #     p = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
    #     if p.match(mobile):
    #         # 这里还可以返回外键
    #         return mobile
    #     raise forms.ValidationError('手机号码格式不对', code='mobile_inval')
