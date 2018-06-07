#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic.base import View

# Create your views here.


class CoursesListView(View):
    """课程列表"""
    def get(self,request):
        return render(request, 'course-list.html')


class CourseDetailView(View):
    """课程详情"""
    def get(self,request,course_id):
        return render(request,'course-detail.html')