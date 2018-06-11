# _*_ coding:utf-8 _*_
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """后台管理显示名称"""
    name = 'users'
    # name = '用户信息'
    verbose_name = '用户信息'  # 配置后台管理显示的APP名称
