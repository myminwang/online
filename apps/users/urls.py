#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "问道编程"
__date__ = "5/29/18 19:27"

from django.conf.urls import url

from .views import RegisterView

urlpatterns = [
    # 用户注册
    url(r'^register/$', RegisterView.as_view(), name='register'),
]