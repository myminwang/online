#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "问道编程"
__date__ = "5/29/18 19:27"

from django.urls import path

from .views import RegisterView, LoginView, RegisterActiveView, UserInfoView, ForgetpwdView, PwdresetView, PwdmodifyView, LogoutView

urlpatterns = [
    # 用户注册
    path('register/', RegisterView.as_view(), name='register'),
    # 用户登录
    path('login/', LoginView.as_view(), name='login'),
    # 注册激活链接
    path('active/<url_active_code>/', RegisterActiveView.as_view()),
    # 个人中心
    path('userinfo/', UserInfoView.as_view(), name='userinfo'),
    # 忘记密码
    path('forgetpwd/', ForgetpwdView.as_view(), name='forgetpwd'),
    # 重置密码链接
    path('pwdreset/<url_pwdreset_code>/', PwdresetView.as_view(), name='pwdreset'),
    # 重置密码处理
    path('pwdmodify/', PwdmodifyView.as_view(), name='pwdmodify'),
    # 注销登录/登出
    path('logout/', LogoutView.as_view(), name='logout'),

]