#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "问道编程"
__date__ = "5/29/18 19:27"

from django.conf.urls import url
from django.urls import path


from .views import CoursesListView, CourseDetailView, CourseVideoView, CourseCommentView

urlpatterns = [
    # 课程列表
    path('list/', CoursesListView.as_view(), name='list'),

    # 课程详情
    path('detail/<int:course_id>/', CourseDetailView.as_view(), name='detail'),

    # 章节列表，点击开始学习时出现的视频列表
    path('video/<int:course_id>/', CourseVideoView.as_view(), name='video'),

    # 课程评论
    path('comment/<int:course_id>/', CourseCommentView.as_view(), name='comment'),

]