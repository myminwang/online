#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "问道编程"
__date__ = "5/29/18 19:27"

from django.urls import path

from .views import RegisterView, LoginView, RegisterActiveView

urlpatterns = [
    # 用户注册
    path('register/', RegisterView.as_view(), name='register'),
    # 用户登录
    path('login/', LoginView.as_view(), name='login'),
    # 注册激活链接
    path('active/<active_code>/', RegisterActiveView.as_view()),
]