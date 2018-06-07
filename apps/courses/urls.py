#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "问道编程"
__date__ = "5/29/18 19:27"

from django.conf.urls import url
from django.urls import path


from .views import CoursesListView, CourseDetailView

urlpatterns = [
    # 课程列表
    path('list/', CoursesListView.as_view(), name='list'),

    # 课程详情
    path('detail/<int:course_id>/', CourseDetailView.as_view(), name='detail'),

]