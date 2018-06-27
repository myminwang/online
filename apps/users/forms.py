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
