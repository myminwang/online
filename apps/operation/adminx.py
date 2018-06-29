#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "问道编程"
__date__ = "5/29/18 17:33"

import xadmin

from .models import CourseComments,UserFav,UserMessage,UserCourse,UserAsk


class CourseCommentsAdmin:
    """课程评论管理"""

    list_display = ['course', 'user', 'comments', 'add_time']
    list_filter = ['course', 'user', 'comments']
    search_fields = ['course', 'user', 'comments', 'add_time']
    model_icon = 'fa fa-comments'


class UserFavAdmin:
    """用户收藏管理"""
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    list_filter = ['user', 'fav_id', 'fav_type']
    search_fields = ['user', 'fav_id', 'fav_type', 'add_time']
    model_icon = 'fa fa-star'


class UserMessageAdmin:
    """用户消息管理"""
    list_display = ['user_name', 'messages', 'add_time', 'has_read']
    list_filter = ['has_read']
    search_fields = ['add_time', 'has_read']
    model_icon = 'fa fa-commenting'


class UserCourseAdmin:
    """用户学习的课程管理"""
    list_display = ['course', 'user', 'add_time']
    list_filter = ['course', 'user']
    search_fields = ['course', 'user', 'add_time']
    model_icon = 'fa fa-leanpub'


class UserAskAdmin:
    """用户咨询管理"""
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    list_filter = ['name', 'mobile', 'course_name']
    search_fields = ['name', 'mobile', 'course_name', 'add_time']
    model_icon = 'fa fa-question-circle'

xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFav, UserFavAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserAsk, UserAskAdmin)