#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "问道编程"
__date__ = "5/29/18 16:52"

import xadmin

from .models import Courseinfo, Lession, Video, CourseResource, CourseBanner
from organizations.models import Organizationinfo


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
    # refresh_times = [3,5]   # 设定页面刷新
    # style_fields = {'detail':'ueditor'}

    def queryset(self):
        """筛选非轮播课程"""
        qs = super(CourseinfoAdmin,self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        """在保存课程时，修改机构的课程总数"""
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Courseinfo.objects.filter(course_org=course_org).count()
            course_org.save()


class CourseBannerAdmin:
    """课程信息管理-轮播课程"""
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

    def queryset(self):
        """筛选轮播课程"""
        qs = super(CourseBannerAdmin,self).queryset()
        qs = qs.filter(is_banner=True)
        return qs

    def save_models(self):
        """在保存课程时，修改机构的课程总数"""
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Courseinfo.objects.filter(course_org=course_org).count()
            course_org.save()


class LessionAdmin:
    """章节管理"""
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
xadmin.site.register(CourseBanner, CourseBannerAdmin)
xadmin.site.register(Lession, LessionAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
