#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "问道编程"
__date__ = "5/29/18 17:33"

import xadmin

from .models import CourseComments,UserFav,UserMessage,UserCourse,UserAsk


class CourseCommentsAdmin:
    """课程评论管理"""

    list_display = ['course', 'users', 'comments', 'add_time']
    list_filter = ['course', 'users', 'comments']
    search_fields = ['course', 'users', 'comments', 'add_time']


class UserFavAdmin:
    """用户收藏管理"""
    list_display = ['users', 'fav_id', 'fav_type', 'add_time']
    list_filter = ['users', 'fav_id', 'fav_type']
    search_fields = ['users', 'fav_id', 'fav_type', 'add_time']


class UserMessageAdmin:
    """用户消息管理"""
    list_display = ['users', 'messages', 'add_time', 'has_read']
    list_filter = ['users', 'messages', 'has_read']
    search_fields = ['users', 'messages', 'add_time', 'has_read']


class UserCourseAdmin:
    """用户学习的课程管理"""
    list_display = ['course', 'users', 'add_time']
    list_filter = ['course', 'users']
    search_fields = ['course', 'users', 'add_time']


class UserAskAdmin:
    """用户咨询管理"""
    list_display = ['name', 'mobile', 'course', 'add_time']
    list_filter = ['name', 'mobile', 'course']
    search_fields = ['name', 'mobile', 'course', 'add_time']


xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFav, UserFavAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserAsk, UserAskAdmin)