#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "问道编程"
__date__ = "5/29/18 17:48"

import xadmin

from .models import City, Organizationinfo, Teacher


class CityAdmin:
    """城市管理"""
    list_display = ['name', 'add_time']
    list_filter = ['name']
    search_fields = ['name', 'add_time']


class OrganizationinfoAdmin:
    """机构信息管理"""
    list_display = ['category', 'city', 'name', 'users', 'students',
                    'address', 'desc', 'add_time', 'tag', 'click_nums', 'fav_nums']
    list_filter = ['category', 'city', 'name', 'students',
                   'address', 'desc', 'tag', 'click_nums', 'fav_nums']
    search_fields = ['category', 'city', 'name', 'students',
                     'address', 'desc', 'add_time', 'tag', 'click_nums', 'fav_nums']


class TeacherAdmin:
    """讲师信息管理"""
    list_display = ['org', 'name', 'users', 'age', 'work_years', 'work_position',
                    'teach_points', 'fav_nums', 'add_time', 'click_nums']
    list_filter = ['org', 'name', 'users', 'age', 'work_years', 'work_position',
                   'teach_points', 'fav_nums', 'click_nums']
    search_fields = ['org', 'name', 'users', 'age', 'work_years', 'work_position',
                     'teach_points', 'fav_nums', 'add_time', 'click_nums']


xadmin.site.register(City, CityAdmin)
xadmin.site.register(Organizationinfo, OrganizationinfoAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
