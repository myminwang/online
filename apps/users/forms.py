#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "问道编程"
__date__ = "5/30/18 12:31"

from django import forms

from captcha.fields import CaptchaField   # 验证码验证模块


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