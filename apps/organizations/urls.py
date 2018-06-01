#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "问道编程"
__date__ = "5/29/18 19:27"

from django.conf.urls import url
from django.urls import path
from .views import TeacherListView, OrgListView

urlpatterns = [
    # 讲师列表
    path('teach_list/', TeacherListView.as_view(), name='teach_list'),

    # 机构列表
    path('org_list/', OrgListView.as_view(), name='org_list'),
]