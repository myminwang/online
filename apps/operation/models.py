# _*_ coding:utf-8 _*_
# 此APP为用户管理模块
from datetime import datetime

from django.db import models

from apps.courses.models import Courseinfo
from apps.users.models import UserProfile
from apps.organizations.models import Organizationinfo, Teacher


# Create your models here.


class CourseComments(models.Model):
    """用户对课程的评论"""
    course = models.ForeignKey(Courseinfo, on_delete=models.SET_NULL, null=True, verbose_name='课程')
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, verbose_name='用户')
    comments = models.TextField(verbose_name='评论')
    add_time = models.DateField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name


class UserFav(models.Model):
    """用户对机构、讲师、课程收藏"""
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, verbose_name='用户')
    fav_id = models.IntegerField(verbose_name='收藏类型的ID', default=0)
    # 该fav_id记录的是相应收藏类型的id
    fav_type = models.IntegerField(verbose_name='收藏类型',
                                   choices=((0, '课程'), (1, '机构'), (2, '讲师')),
                                   default=0)
    add_time = models.DateField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    """
    用户消息
    系统对用户的消息分为对单个用户的、对全部用户的
    """
    # 如果 为 0 代表全局消息，否则就是用户的 ID
    user = models.IntegerField(default=0, verbose_name='接收用户')
    messages = models.CharField(verbose_name='消息内容', max_length=500)
    add_time = models.DateField(verbose_name='添加时间', default=datetime.now)

    has_read = models.BooleanField(verbose_name='是否已读', default=False)

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name

# 用户对用户的消息


class UserCourse(CourseComments):
    """用户正在学习的课程,继承用户评论"""
    class Meta:
        verbose_name = '用户学习的课程'
        verbose_name_plural = verbose_name


class UserAsk(models.Model):
    """用户咨询"""
    name = models.CharField(verbose_name='姓名',max_length=50)
    mobile = models.CharField(verbose_name='联系电话',max_length=11)
    course = models.CharField(verbose_name='课程名',max_length=100)
    add_time = models.DateField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name


# 用户对课程、讲师、课程点赞
