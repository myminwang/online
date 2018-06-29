#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "问道编程"
__date__ = "5/29/18 10:41"

import xadmin
from xadmin import views

from .models import EmailVerification, Banner


class BaseSetting:
    """
    后台修改需要的配置
    """
    enable_themes = True  # 开启主题功能
    use_bootswatch = True


class GlobalSettings:
    """
    后台修改
    """
    site_title = '在线学习网'
    site_footer = '在线学习网'
    menu_style = 'accordion'  # 开启分组折叠


class EmailVerificationAdmin:
    """邮箱验证后台管理"""
    list_display = ['email', 'code', 'send_type', 'send_time', 'is_delete']
    list_filter = ['email', 'code', 'send_type']
    search_fields = ['email', 'code', 'send_type', 'send_time', 'is_delete']
    fields = ['send_type', 'email', 'code', 'is_delete']


class BannerAdmin:
    """轮播图后台管理"""
    list_display = ['order', 'image', 'banner_url', 'add_time', 'go_to']
    list_filter = ['image', 'banner_url', 'order']
    search_fields = ['image', 'banner_url', 'order', 'add_time']
    fields = ['image', 'banner_url', 'order']


xadmin.site.register(EmailVerification, EmailVerificationAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
