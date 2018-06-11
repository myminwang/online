#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "问道编程"
__date__ = "5/29/18 10:41"

# 使用xadmin时，首先在配置里注册，修改URL，在每个APP下修改apps.py __init__.py两个文件显示中文目录
import xadmin
from xadmin import views  # 使用views下的模块注册基础配置

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
    site_title = '后台管理系统'
    site_footer = '在线学习网'
    menu_style = 'accordion'  # 开启分组折叠


class EmailVerificationAdmin:
    """邮箱验证后台管理"""
    list_display = ['email', 'code', 'send_type', 'send_time', 'is_delete']
    list_filter = ['email', 'code', 'send_type']
    search_fields = ['email', 'code', 'send_type', 'send_time', 'is_delete']
    fields = ['send_type', 'email', 'code', 'is_delete']


class BannerAdmin:           # python2.7 需要继承object，是新类，3.x后不需要声明，也会继承新类
    """轮播图后台管理"""
    list_display = ['order', 'image', 'banner_url', 'add_time']
    list_filter = ['image', 'banner_url', 'order']
    search_fields = ['image', 'banner_url', 'order', 'add_time']
    fields = ['image', 'banner_url', 'order']


# xadmin.site.register(UserProfile, UserProfileAdmin)  # 默认是注册的
xadmin.site.register(EmailVerification, EmailVerificationAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
