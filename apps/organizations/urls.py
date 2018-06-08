#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "问道编程"
__date__ = "5/29/18 19:27"

from django.conf.urls import url
from django.urls import path
from .views import TeacherListView, OrgListView, OrgHomeView, UserAskView, OrgCourseView, OrgTeacherListView, \
    OrgDescView, TeacherDetailView

urlpatterns = [
    # 教师列表
    path('teach_list/', TeacherListView.as_view(), name='teach_list'),

    # 教师详情
    path('teacher_detail/<int:teacher_id>/', TeacherDetailView.as_view(), name='teacher_detail'),

    # 机构列表
    path('org_list/', OrgListView.as_view(), name='org_list'),

    # 机构首页
    path('org_home/<int:org_id>/', OrgHomeView.as_view(), name='org_home'),

    # 用户咨询
    path('user_ask/', UserAskView.as_view(), name='user_ask'),

    # 机构课程
    path('org_course/<int:org_id>/', OrgCourseView.as_view(), name='org_course'),

    # 机构教师
    path('org_teacher/<int:org_id>/', OrgTeacherListView.as_view(), name='org_teacher'),

    # 机构介绍
    path('org_desc/<int:org_id>/', OrgDescView.as_view(), name='org_desc'),
]
