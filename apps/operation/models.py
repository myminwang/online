# _*_ coding:utf-8 _*_
# 此APP为用户管理模块
from datetime import datetime

from django.db import models
from courses.models import Courseinfo
from users.models import UserProfile


# Create your models here.


class CourseComments(models.Model):
    """用户对课程的评论"""
    course = models.ForeignKey(Courseinfo, on_delete=models.CASCADE, null=True, verbose_name='课程')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, verbose_name='用户')
    comments = models.TextField(verbose_name='评论')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name


class UserFav(models.Model):
    """用户对机构、教师、课程收藏"""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    fav_id = models.IntegerField(verbose_name='收藏类型的ID', default=0)
    # 该fav_id记录的是相应收藏类型的id
    fav_type = models.IntegerField(verbose_name='收藏类型',
                                   choices=((0, '课程'), (1, '机构'), (2, '教师')),
                                   default=0)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    """
    用户消息
    系统对用户的消息分为对单个用户的、对全部用户的
    """
    # 如果 为 0 代表全局消息，否则就是用户的 ID
    user_id = models.IntegerField(default=0, verbose_name='接收用户')
    messages = models.CharField(verbose_name='消息内容', max_length=500)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    has_read = models.BooleanField(verbose_name='是否已读', default=False)

    def user_name(self):
        if self.user_id != 0:
            return UserProfile.objects.get(id=self.user_id)
        else:
            return '系统消息'
    user_name.short_description = '接收用户'

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    """用户正在学习的课程,可以继承用户评论"""
    course = models.ForeignKey(Courseinfo, on_delete=models.CASCADE, null=True, verbose_name='课程')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, verbose_name='用户')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户学习的课程'
        verbose_name_plural = verbose_name


class UserAsk(models.Model):
    """用户咨询"""
    name = models.CharField(verbose_name='姓名', max_length=50)
    mobile = models.CharField(verbose_name='联系电话', max_length=11)
    course_name = models.CharField(verbose_name='课程名', max_length=100)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)
    is_delete = models.BooleanField(verbose_name='是否已处理', default=0, choices=((0, '未处理'), (1, '已处理')))

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name
