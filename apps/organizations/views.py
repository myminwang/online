#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic.base import View

# Create your views here.


class TeacherListView(View):
    """讲师列表"""
    pass


class OrgListView(View):
    """机构列表"""

    # def get(self,request):
    #     """进入机构列表页"""
    #     return render(request,'org-list.html' ,{})
    pass
