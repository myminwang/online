#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "问道编程"
__date__ = "5/29/18 17:48"

import xadmin

from .models import City, Organizationinfo, Teacher


class CityAdmin:
    """城市管理"""
    list_display = ['name', 'add_time']
    search_fields = ['name', 'add_time']
    fields = ['name']
    list_per_page = 20


class OrganizationinfoAdmin:
    """机构信息管理"""
    list_display = ['name', 'city', 'address', 'category', 'add_time', 'desc', 'tag', 'students',
                    'click_nums', 'fav_nums', 'teacher_nums', 'course_nums']
    list_filter = ['name', 'city', 'category', 'tag']
    search_fields = ['name']
    fields = ['name', 'category', 'city', 'address', 'image', 'desc', 'tag', 'is_authentication', 'is_gold']
    list_per_page = 10


class TeacherAdmin:
    """教师信息管理"""
    list_display = ['name', 'age', 'org', 'work_position', 'work_years',
                    'teach_points', 'add_time', 'fav_nums', 'click_nums', 'course_nums']
    list_filter = ['org', 'name', 'age', 'work_years']
    search_fields = ['org', 'name']
    fields = ['name', 'age', 'org', 'work_position', 'work_years', 'image',
              'teach_points']
    list_per_page = 10


xadmin.site.register(City, CityAdmin)
xadmin.site.register(Organizationinfo, OrganizationinfoAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
