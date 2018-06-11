#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "问道编程"
__date__ = "5/29/18 16:52"

import xadmin

from .models import Courseinfo, Lession, Video, CourseResource


class LessonInline:
    """添加课程的时候可以顺便添加章节"""
    model = Lession
    readonly_fields = ['add_time']
    extra = 0


class CourseResourceInline:
    """添加课程的时候可以顺便添加课程资源"""
    model = CourseResource
    readonly_fields = ['add_time']
    extra = 0


class CourseinfoAdmin:
    """课程信息管理"""
    list_display = ['name', 'teacher', 'course_org', 'desc',
                    'category', 'degree', 'learn_time', 'students', 'fav_nums',
                    'click_nums', 'is_banner', 'add_time']
    list_filter = ['course_org', 'teacher', 'name', 'image', 'desc',
                   'degree', 'students', 'learn_time', 'category', 'fav_nums',
                   'click_nums', 'detail', 'is_banner', 'before_know', 'teacher_tell']
    search_fields = ['course_org', 'teacher', 'name', 'image', 'desc',
                     'degree', 'students', 'learn_time', 'category', 'fav_nums',
                     'click_nums', 'detail', 'is_banner', 'before_know', 'teacher_tell', 'add_time']
    readonly_fields = ['fav_nums', 'click_nums', 'students', 'add_time']
    inlines = [LessonInline, CourseResourceInline]


class LessionAdmin:
    """课程轮播图管理"""
    list_display = ['course', 'name', 'add_time']
    list_filter = ['course', 'name']
    search_fields = ['course', 'name', 'add_time']
    readonly_fields = ['add_time']


class VideoAdmin:
    """课程小节/视频管理"""
    list_display = ['lession', 'name', 'url', 'learn_time', 'add_time']
    list_filter = ['lession', 'name', 'url', 'learn_time']
    search_fields = ['lession', 'name', 'url', 'learn_time', 'add_time']
    readonly_fields = ['add_time']


class CourseResourceAdmin:
    """课程资料管理"""
    list_display = ['lession', 'name', 'download', 'add_time']
    list_filter = ['lession', 'name', 'download']
    search_fields = ['lession', 'name', 'download', 'add_time']
    readonly_fields = ['add_time']


xadmin.site.register(Courseinfo, CourseinfoAdmin)
xadmin.site.register(Lession, LessionAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
